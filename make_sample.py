"""make_sample.py - create made-up practice text files for the lesson.

Creates a folder called "sample" next to this script with five small
made-up text files saved with different line-ending styles, plus one
extra file in a subfolder (the tool stays at the top level, so that
one is not counted). It refuses any existing sample path before writing.
Nothing is deleted or replaced.
"""
import os
import stat
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE = os.path.join(HERE, "sample")

JOURNAL = "\n".join("Entry %02d" % n for n in range(1, 13))  # no final newline

FILES = [
    ("ideas.txt", b"Buy milk\n\nCall Sam\nWater the plants\n"),
    ("journal.txt", JOURNAL.encode("utf-8")),
    ("old_mac.txt", b"alpha\rbeta\rgamma\r"),
    ("scratch.txt", b""),
    ("windows.txt", b"one\r\n\r\ntwo\r\n\r\nthree\r\n"),
    ("sub/inner.txt", b"hidden in a subfolder\n"),
]


def main():
    root = Path(SAMPLE).absolute()
    if '..' in root.parts:
        raise OSError('Parent-traversal paths are unsupported.')
    for parent in reversed(root.parents):
        info = parent.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise OSError('Linked/reparse-point parents are unsupported.')
    try:
        os.mkdir(SAMPLE)
    except FileExistsError:
        raise SystemExit("Stopped: sample already exists. Nothing was replaced or deleted.")
    for relative, data in FILES:
        path = os.path.join(SAMPLE, *relative.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "xb") as handle:
            handle.write(data)
    print("Created a new sample folder beside make_sample.py.")
    print("It holds 5 made-up text files, plus 1 more in a subfolder.")


if __name__ == "__main__":
    main()
