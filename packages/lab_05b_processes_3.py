from __future__ import annotations

import glob
import subprocess
import sys

if __name__ == "__main__":
    path = ".\\scripts\\"

    success = []
    failure = []

    for script in glob.glob(path + "*.py"):

        try:
            subprocess.run(
                ["python", script],
                shell=True,
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                check=True,
            )
            success.append(script)
        except subprocess.CalledProcessError:
            failure.append(script)

    print(f"{success=}")
    print(f"{failure=}")
