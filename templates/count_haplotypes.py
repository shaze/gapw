#!/usr/bin/python

from __future__ import print_function

import  sys

if len(sys.argv)==1:
    sys.argv=["count_haplotypes.py","$fam","$numhaplos"]

LF=unichr(10)

f = open(sys.argv[1])
n = len(f.readlines())
f.close()
f = open(sys.argv[2],"w")
f.write("%d%s"%(n*2,LF))
f.close()


