# Text file line counter

`count_lines.py` counts the lines in the `.txt` files directly inside
one folder and shows a small table, so you can see at a glance which
notes are empty and which are long. It is read-only: it only looks,
and it never changes, moves or deletes anything. Run it first on the
made-up `sample` folder from `make_sample.py` before pointing it
anywhere else.

- Windows (CRLF), Mac/Linux (LF) and old Mac (CR) endings all count,
  and a last line without an ending still counts.
- A blank line is a line with no characters at all; a line of only
  spaces is not blank.
- Only the top level of the folder is counted; subfolders are not
  entered. Files that are not valid UTF-8 text are skipped, with a
  note at the end.

## Use

    python make_sample.py
    python count_lines.py sample
    python count_lines.py "C:\Users\you\Documents"

If you leave out the folder, the current folder is counted.

## Tests

    python -m unittest -v

Works on Windows, Mac and Linux with Python 3.10 or newer. Nothing to
install: it uses only what comes with Python.

## License

MIT (see LICENSE).
