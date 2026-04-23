from pathlib import Path
import shutil
import os
import sys

SHARE = os.environ["JS_ASSETS"]
BUILD_SHARE = Path(os.environ["BUILD_PREFIX"]) / SHARE
PREFIX_SHARE = Path(os.environ["PREFIX"]) / SHARE
SRC_DIR = Path(os.environ["SRC_DIR"])


def main() -> int:
    PREFIX_SHARE.parent.mkdir(parents=True)
    shutil.copytree(BUILD_SHARE, PREFIX_SHARE)
    third_party = PREFIX_SHARE / "static/third-party-licenses.json"
    shutil.copy2(third_party, SRC_DIR / third_party.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
