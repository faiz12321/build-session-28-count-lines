# Count lines in text files

Read-only teaching tool. Counts UTF-8 .txt files directly inside a folder,
not subfolders. It uses str.splitlines, so it recognizes more line boundaries
than LF, CR and CRLF. A last line without an ending counts; an empty line has
no characters, while spaces-only lines are not blank. Invalid UTF-8 files are
skipped. This is not a count of visually wrapped lines in an editor.

File links are followed: a .txt link can read a target outside the chosen
folder. Link handling is unchanged and is not covered by these fixture tests.

## Practise

Save all three files in a new empty lesson folder. Python 3 is required:

    python make_sample.py
    python count_lines.py sample
    python -m unittest -v

Setup creates sample beside the script and refuses any existing sample path.
It never deletes or resets an old sample. Use a different new empty lesson
folder if it refuses. The contents are fictional text for line-count practice.

## Evidence

24 tests use temporary fixtures, including the sample-count test. They cover
line counting, CLI errors, unchanged source sizes/times, setup refusal for an
existing file/folder, original bytes, nested sentinel data and repeat-run
preservation. These are limited fixture checks, not universal safety proof.

Two GitHub-hosted Windows recordings and two Ubuntu recordings pass all tests.
The driver first saves the newline-character counter and records its undercount,
then saves the final line counter, as the lesson shows. Displayed output uses
first Windows output. Paired runs differ only in unittest elapsed time. Versions
and test rendering can differ. No Windows desktop or macOS session was tested.

## License

MIT (see LICENSE).
