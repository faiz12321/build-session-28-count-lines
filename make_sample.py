"""make_sample.py - create made-up practice text files for the lesson.

Creates a folder called "sample" next to this script with five small
made-up text files saved with different line-ending styles, plus one
extra file in a subfolder (the tool stays at the top level, so that
one is not counted). Run it again any time; it first removes the old
sample folder.
"""
import os
import shutil

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
    if os.path.isdir(SAMPLE):
        shutil.rmtree(SAMPLE)
    for relative, data in FILES:
        path = os.path.join(SAMPLE, *relative.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as handle:
            handle.write(data)
    print("Sample folder ready: " + SAMPLE)
    print("It holds 5 made-up text files, plus 1 more in a subfolder.")


if __name__ == "__main__":
    main()
