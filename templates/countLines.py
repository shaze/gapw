#!/usr/bin/env python

from __future__ import print_function
import sys

if len(sys.argv)==1:
    sys.argv=["countLines.py","$inp","$out"]

def countLines(fn):
    count=0
    with open(fn) as f:
        for  line in f:
            count=count+1
    return count

n=countLines(sys.argv[1])
g=open(sys.argv[2],"w")
g.write("%d%s"%(n,LF))
g.close()
