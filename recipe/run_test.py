"""Check a labextension for path length and detected lab status."""

import sys
from subprocess import Popen, PIPE
import re
from pathlib import Path
import os

#: historically informed by 125 character `package.json.orig`
PATH_LENGTH_MAX = 128
PREFIX = Path(sys.prefix)
JS_NAME = os.environ["JS_NAME"]
SHARE = PREFIX / "share/jupyter/labextensions" / JS_NAME


def check_bad_paths() -> int:
    """Ensure paths are short enough for windows."""
    paths = [p.relative_to(PREFIX).as_posix() for p in sorted(SHARE.rglob("*"))]
    if not paths:
        print(f"!!! no paths found in {SHARE}")
        return 2
    bad_paths = [p for p in paths if len(p) > PATH_LENGTH_MAX]
    if bad_paths:
        print("\n".join(bad_paths))
        print(f"!!! {len(bad_paths)} are too long for windows")
        return 3
    print(f"... OK no paths longer than {PATH_LENGTH_MAX} found")
    return 0


def do(args: list[str], expect_output: str | None = None) -> int:
    """Run a command, check for output."""
    print(">>>", *args)
    proc = Popen(args, stdout=PIPE, stderr=PIPE, encoding="utf-8")
    stdout, stderr = proc.communicate()
    rc = proc.returncode
    if expect_output:
        if re.search(expect_output, f"{stdout}\n{stderr}"):
            print(f"... OK found expected pattern {expect_output}")
        else:
            print("STDOUT", stdout)
            print("STDERR", stderr)
            print("!!! missing", expect_output)
            rc = 4
    return rc


if __name__ == "__main__":
    rcs = [
        check_bad_paths(),
        do(["jupyter", "labextension", "list", "--debug"], rf"{JS_NAME}.*OK"),
    ]
    sys.exit(max(rcs))
