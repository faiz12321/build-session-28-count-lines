"""count_lines.py - count the lines in the text files of one folder.

Read-only: it only looks. It never changes, moves or deletes anything.

Only files ending in .txt directly inside the folder are counted;
subfolders are not entered. Lines are split the way Python's
str.splitlines() splits them, so Windows (CRLF), Mac/Linux (LF) and
old Mac (CR) endings all count, and a last line without an ending
still counts. A blank line is a line with no characters at all; a
line of only spaces is not blank. Files that are not valid UTF-8
text are skipped, with a note at the end.

Usage:
    python count_lines.py [FOLDER]
FOLDER defaults to the current folder.
"""
import os
import sys


def count_file(path):
    """Return (total, blank) line counts for one UTF-8 text file."""
    with open(path, "rb") as handle:
        data = handle.read()
    lines = data.decode("utf-8").splitlines()
    blank = sum(1 for line in lines if line == "")
    return len(lines), blank


def scan_folder(root):
    """Return (rows, skipped) for the .txt files directly inside root.

    rows holds (name, total, blank), sorted by name ignoring case.
    skipped holds names that could not be read as UTF-8 text."""
    rows = []
    skipped = []
    for name in sorted(os.listdir(root), key=str.lower):
        full = os.path.join(root, name)
        if not os.path.isfile(full) or not name.lower().endswith(".txt"):
            continue
        try:
            total, blank = count_file(full)
        except (OSError, UnicodeDecodeError):
            skipped.append(name)
            continue
        rows.append((name, total, blank))
    return rows, skipped


def main(argv):
    if len(argv) > 2 or (len(argv) == 2 and argv[1] in ("-h", "--help")):
        print("Usage: python count_lines.py [FOLDER]", file=sys.stderr)
        return 2
    root = argv[1] if len(argv) == 2 else "."
    if not os.path.isdir(root):
        print("No such folder: " + root, file=sys.stderr)
        return 2
    rows, skipped = scan_folder(root)
    print("Line counts")
    print("Folder: " + root)
    print()
    if not rows:
        if skipped:
            print("No readable .txt files here.")
        else:
            print("No .txt files here.")
    else:
        print("lines  blank  file")
        print("-----  -----  ----")
        files = 0
        total_lines = 0
        total_blank = 0
        for name, total, blank in rows:
            print("%5d  %5d  %s" % (total, blank, name))
            files += 1
            total_lines += total
            total_blank += blank
        print()
        word = "file" if files == 1 else "files"
        print("%d %s counted: %d lines in total, %d blank."
              % (files, word, total_lines, total_blank))
    if skipped:
        word = "file" if len(skipped) == 1 else "files"
        print("%d %s skipped (not plain UTF-8 text): %s"
              % (len(skipped), word, ", ".join(skipped)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
