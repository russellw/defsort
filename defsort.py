import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="count", help="increase output verbosity")
parser.add_argument("files", nargs="*")
args = parser.parse_args()


def do(filename):
    if args.verbose:
        print(filename)
    v = [s.rstrip() for s in open(filename, encoding="utf-8")]
    print(v)


for f in args.files:
    for root, dirs, files in os.walk(f):
        for filename in files:
            if os.path.splitext(filename)[1] == ".py":
                do(os.path.join(root, filename))
