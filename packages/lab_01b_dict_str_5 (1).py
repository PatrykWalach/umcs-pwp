from __future__ import annotations

import logging
import shutil
import sys

try:
    shutil.copyfile(sys.argv[1], sys.argv[2])
except Exception as e:
    logging.exception(e)
