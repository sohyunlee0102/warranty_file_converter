import os
import sys


def getResourcePath(relativePath: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relativePath)
    return os.path.abspath(relativePath)
