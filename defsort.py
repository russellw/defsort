import argparse
import inspect
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="count", help="increase output verbosity")
parser.add_argument("files", nargs="*")
args = parser.parse_args()


def dbg(a):
    info = inspect.getframeinfo(inspect.currentframe().f_back)
    sys.stderr.write(f"{info.filename}:{info.function}:{info.lineno}: {a}\n")


def parse(v, i):
    dent = indent(v, i)
    j = i + 1
    while indent(v, j) > dent:
        j += 1
    return v[i:j]


def indent(v, i):
    if i == len(v):
        return -1
    s = v[i]
    j = 0
    while s[j] == " ":
        j += 1
    if s[j] == "\n":
        return 1000000
    if s[j] == "\t":
        raise Exception("file indented with tabs")
    return j


def is_def(s):
    return s.lstrip().startswith("def ")


def do(filename):
    if args.verbose:
        print(filename, end=": ")
    v = open(filename, encoding="utf-8").readlines()
    old = v.copy()
    for i in range(len(v)):
        if is_def(v[i]):
            j = i
            ds = []
            while is_def(v[j]):
                d = parse(v, j)
                j += len(d)
                ds.append(d)
            ds.sort()
            v[i:j] = flatten(ds)
    if v == old:
        if args.verbose:
            print("unchanged")
    else:
        if args.verbose:
            print("sorted")
        open(filename, "w", newline="\n").writelines(v)


def flatten(ds):
    v = []
    for d in ds:
        v.extend(d)
    return v


for f in args.files:
    for root, dirs, files in os.walk(f):
        for filename in files:
            if os.path.splitext(filename)[1] == ".py":
                do(os.path.join(root, filename))
