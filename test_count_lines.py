"""Tests for count_lines.py. They run in a temporary folder, so real
files are never touched."""
import contextlib
import io
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

import count_lines

HERE = os.path.dirname(os.path.abspath(__file__))


def run_main(args):
    out = io.StringIO()
    err = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = count_lines.main(args)
    return rc, out.getvalue(), err.getvalue()


class Base(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def write(self, relative, data):
        path = os.path.join(self.dir, *relative.split("/"))
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(path, "wb") as handle:
            handle.write(data)
        return path


class CountFileTests(Base):
    def test_lf_endings(self):
        self.assertEqual(count_lines.count_file(self.write("a.txt", b"a\nb\n")), (2, 0))

    def test_last_line_without_ending_still_counts(self):
        self.assertEqual(count_lines.count_file(self.write("a.txt", b"a\nb")), (2, 0))

    def test_crlf_endings(self):
        self.assertEqual(count_lines.count_file(self.write("a.txt", b"a\r\nb\r\n")), (2, 0))

    def test_cr_only_endings(self):
        self.assertEqual(count_lines.count_file(self.write("a.txt", b"a\rb\r")), (2, 0))

    def test_blank_lines(self):
        self.assertEqual(count_lines.count_file(self.write("a.txt", b"a\n\nb\n")), (3, 1))

    def test_spaces_only_line_is_not_blank(self):
        self.assertEqual(count_lines.count_file(self.write("a.txt", b"a\n   \nb\n")), (3, 0))

    def test_empty_file(self):
        self.assertEqual(count_lines.count_file(self.write("a.txt", b"")), (0, 0))

    def test_non_utf8_raises(self):
        with self.assertRaises(UnicodeDecodeError):
            count_lines.count_file(self.write("a.txt", b"\xff\xfe not text"))


class ScanFolderTests(Base):
    def test_subfolders_are_not_entered(self):
        self.write("top.txt", b"a\n")
        self.write("sub/inner.txt", b"x\ny\nz\n")
        rows, skipped = count_lines.scan_folder(self.dir)
        self.assertEqual(rows, [("top.txt", 1, 0)])
        self.assertEqual(skipped, [])

    def test_non_txt_files_are_ignored(self):
        self.write("data.csv", b"a,b\n")
        self.write("notes.txt", b"a\n")
        rows, _ = count_lines.scan_folder(self.dir)
        self.assertEqual([row[0] for row in rows], ["notes.txt"])

    def test_uppercase_extension_counts(self):
        self.write("NOTES.TXT", b"a\n")
        rows, _ = count_lines.scan_folder(self.dir)
        self.assertEqual([row[0] for row in rows], ["NOTES.TXT"])

    def test_unreadable_file_is_skipped(self):
        self.write("good.txt", b"a\n")
        self.write("odd.txt", b"\xff\xfe not text")
        rows, skipped = count_lines.scan_folder(self.dir)
        self.assertEqual([row[0] for row in rows], ["good.txt"])
        self.assertEqual(skipped, ["odd.txt"])

    def test_names_sorted_ignoring_case(self):
        self.write("b.txt", b"b\n")
        self.write("A.txt", b"a\n")
        rows, _ = count_lines.scan_folder(self.dir)
        self.assertEqual([row[0] for row in rows], ["A.txt", "b.txt"])


class MainTests(Base):
    def test_summary_line(self):
        self.write("a.txt", b"a\n\nb\n")
        self.write("b.txt", b"x\n")
        rc, out, _ = run_main(["count_lines.py", self.dir])
        self.assertEqual(rc, 0)
        self.assertIn("2 files counted: 4 lines in total, 1 blank.", out)

    def test_no_txt_files(self):
        self.write("data.csv", b"a,b\n")
        rc, out, _ = run_main(["count_lines.py", self.dir])
        self.assertEqual(rc, 0)
        self.assertIn("No .txt files here.", out)

    def test_only_unreadable_txt(self):
        self.write("odd.txt", b"\xff bad")
        rc, out, _ = run_main(["count_lines.py", self.dir])
        self.assertEqual(rc, 0)
        self.assertIn("No readable .txt files here.", out)
        self.assertIn("1 file skipped (not plain UTF-8 text): odd.txt", out)

    def test_missing_folder(self):
        rc, _, err = run_main(["count_lines.py", os.path.join(self.dir, "nope")])
        self.assertEqual(rc, 2)
        self.assertIn("No such folder", err)

    def test_usage_error(self):
        rc, _, err = run_main(["count_lines.py", "a", "b"])
        self.assertEqual(rc, 2)
        self.assertIn("Usage", err)

    def test_run_leaves_folder_unchanged(self):
        self.write("a.txt", b"a\nb\n")
        self.write("b.txt", b"x\ny\n")
        before = self.snapshot()
        rc, _, _ = run_main(["count_lines.py", self.dir])
        self.assertEqual(rc, 0)
        self.assertEqual(before, self.snapshot())

    def snapshot(self):
        state = {}
        for name in sorted(os.listdir(self.dir)):
            path = os.path.join(self.dir, name)
            state[name] = (os.path.getsize(path), os.path.getmtime(path))
        return state


class SampleTests(unittest.TestCase):
    def test_sample_counts(self):
        subprocess.run([sys.executable, os.path.join(HERE, "make_sample.py")],
                       check=True, capture_output=True)
        rc, out, _ = run_main(["count_lines.py", os.path.join(HERE, "sample")])
        self.assertEqual(rc, 0)
        self.assertIn("5 files counted: 24 lines in total, 3 blank.", out)
        self.assertNotIn("skipped", out)

    def test_source_is_read_only(self):
        with open(os.path.join(HERE, "count_lines.py"), "r") as handle:
            source = handle.read()
        self.assertIn('open(path, "rb")', source)
        for word in ("os.remove", "os.unlink", "os.rename", "os.replace",
                     "os.mkdir", "os.rmdir", "shutil", ".write(", "writelines",
                     '"w")', "'w')", '"a")', "'a')"):
            self.assertNotIn(word, source)


if __name__ == "__main__":
    unittest.main()
