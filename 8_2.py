import subprocess
import sys

dirStr = "K1 _K2 _K3 __K4 K5 _K6"


def depth(s: str) -> int:
    return len(s) - len(s.lstrip("_"))


if __name__ == "__main__":

    dirs = dirStr.split(" ")

    for i, dir in reversed(list(enumerate(dirs))):
        for parent in reversed(dirs[0:i:]):
            if not dir.startswith("_"):
                break

            diff = depth(parent) - depth(dir)
            if diff >= 0:
                continue

            dir = "_" * diff + parent + "\\" + dir.lstrip("_")
            dirs[i] = dir

    dirs = [
        ".\\" + dir
        for dir in dirs
        if len([1 for dir2 in dirs if dir2.startswith(dir)]) == 1
    ]

    for dir in dirs:
        subprocess.run(
            ["mkdir", dir],
            shell=True,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            check=True,
        )
