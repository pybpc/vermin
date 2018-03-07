import sys

from .config import Config
from .printing import nprint
from .detection import detect_paths
from .processing import process_paths
from .arguments import parse_args

def main():
  config = Config.get()
  args = parse_args()
  processes = args["processes"]

  nprint("Detecting python files..")
  paths = set(detect_paths(args["paths"]))
  amount = len(paths)
  if amount == 0:
    print("No files specified to analyze!")
    sys.exit(-1)

  msg = "Analyzing"
  if amount > 1:
    msg += " {} files".format(amount)
  nprint("{} using {} processes..".format(msg, processes))
  (mins, incomp) = process_paths(paths, processes)

  if incomp and not config.ignore_incomp():
    nprint("Note: Some files had incompatible versions so the results might not be correct!")

  incomps = []
  reqs = []
  for i in range(len(mins)):
    ver = mins[i]
    if ver is None:
      incomps.append(str(i + 2))
    elif ver is not None and ver != 0:
      reqs.append(str(ver))

  if len(reqs) == 0 and len(incomps) == 0:
    print("Could not determine minimum required versions!")
  if len(reqs) > 0:
    print("Minimum required versions: {:>5}".format(", ".join(reqs)))
  if len(incomps) > 0:
    print("Incompatible versions:     {:>5}".format(", ".join(incomps)))