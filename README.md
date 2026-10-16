# Count lines in fictional text files

Save three source files in a NEW empty lesson folder.

    python make_sample.py
    python count_lines.py sample
    python -m unittest -v

Two Windows and two Ubuntu full replays run exact visible source versions. Final 38 small fixture tests pass (Unix pipe skips on Windows); symlink creation can skip where unavailable. Displayed stdout is first Windows output, not normalized or mixed. Pair differences are unittest time.
Link/error changes only: refuse root/ancestor and direct-entry symbolic links/reparse points, hardlinks, special files and traversal. Metadata/list/open errors now stop with exit 2 instead of silent skips or false clean counts. Each direct entry is checked, even a non-.txt alias. Setup refuses linked parents/traversal and existing sample paths, without reset or deletion. Naive first version remains fictional-sample-only and must be replaced.
Original top-level-only .txt selection, case-insensitive extension, UTF-8 decoding, splitlines and truly-empty-line definition, sort order and totals remain unchanged. Ordinary subfolders are ignored, not entered. Invalid UTF-8 files still list/skip and keep prior exit 0; this is not a complete-count certificate. Spaces-only lines remain nonblank. No unrelated encoding/count rule changed.
The checker has no write/move/delete/network code but reads each counted file into memory. No size/time/resource limit, atomic snapshot or hostile-race defense. Stop editors/sync; entries can change between metadata and read. Filenames can be private. Small fictional fixtures are not proof on every filesystem. No desktop Windows/macOS recording. Recorder removes only its own temporary fixture folder. Decisions and feedback are teaching text, not recorded output.

MIT code. Python separately licensed/not included.

Reference: https://docs.python.org/3/library/os.html

Windows pair: https://github.com/faiz12321/lesson-lab/actions/runs/38976283251
Ubuntu pair: https://github.com/faiz12321/lesson-lab/actions/runs/38976344423
