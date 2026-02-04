from pathlib import Path
import shutil
import sys
import os

SHARE = "share/jupyter/labextensions/@jupyterlab-widgets/jupyterlab-manager"
SRC = Path(os.environ["BUILD_PREFIX"]) / SHARE
DEST = Path(sys.prefix) / SHARE


if __name__ == "__main__":
    DEST.parent.mkdir(parents=True)
    shutil.copytree(SRC, DEST)
