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


def do(file):
    if args.verbose:
        print(file, end=": ")
    v = open(file, encoding="utf-8").readlines()
    old = v.copy()
    i = 0
    while i < len(v):
        if is_def(v, i):
            j = i
            ds = []
            while is_def(v, j):
                d = parse(v, j)
                j += len(d)
                ds.append(d)
            ds.sort()
            v[i:j] = flatten(ds)
            i = j
        else:
            i += 1
    if v == old:
        if args.verbose:
            print("unchanged")
    else:
        if args.verbose:
            print("sorted")
        open(file, "w", newline="\n").writelines(v)


def flatten(ds):
    v = []
    for d in ds:
        v.extend(d)
    return v


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


def is_def(v, i):
    if i == len(v):
        return
    s = v[i]
    return s.lstrip().startswith("def ")


def parse(v, i):
    dent = indent(v, i)
    j = i + 1
    while indent(v, j) > dent:
        j += 1
    return v[i:j]


for f in args.files:
    for root, dirs, files in os.walk(f):
        for file in files:
            if os.path.splitext(file)[1] == ".py":
                do(os.path.join(root, file))
