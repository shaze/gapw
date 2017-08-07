#!/usr/bin/env python
# Takes as input
#  - A file describing an Illumica chip 
#     It should have a header line columns within the first 15 lines "Name Chr MapInfo deCODE(cM):
#     the cm is optional



from __future__ import print_function

import sys
import argparse
import re
from shutil import copyfile

def parseArguments():
    parser=argparse.ArgumentParser()
    parser.add_argument('array', type=str, metavar='samplesheet'),
    parser.add_argument('output', type=str, metavar='fname',help="output base"),
    args = parser.parse_args()
    return args

TAB=unichr(9)
EOL=unichr(10)
# auxiliary defs
chr2chr = map(str,range(0,27))
chr2chr[23]="X"
chr2chr[24]="Y"
chr2chr[25]="XY"
chr2chr[26]="MT"



def conv(x):
   try:
      num = int(x)
   except ValueError:
      if x == "X": num=23
      elif x == "Y": num=24
      elif x == "XY": num =25
      elif x == "MT": num=26
      else: num = 0
   return num

def parseArray(fname):
    f = open(fname)
    for i in range(15):
        line = f.readline()
        if "Name" in line: break
    else:
        sys.exit("Cannot find header line in "+fname)
    fields=re.split("[,\t]",line.rstrip())
    name_i = fields.index("Name")
    indices = [fields.index("Chr"),fields.index("MapInfo")]
    if "deCODE(cM)" in fields:
        indices.append(fields.index("deCODE(cM)"))
    array = {}
    for line in f:
        fields=re.split("[,\t]",line.rstrip())
        curr  =[conv(fields[indices[0]]), int(fields[indices[1]])]
        if len(indices)==3:
            cm = fields[indices[2]]
            cm = 0.0 if  "NA" in cm else float(cm)
            curr.append(cm)
        array[fields[name_i]]=curr
    return array

def parseChipReport(array,fname,output):
    f = open(fname)
    for i in range(15):
        line = f.readline()
        if "SNP Name" in line: break
    else:
        sys.exit("Cannot find header line in "+fname)
    #SNP NameSample IDAllele1 - TopAllele2 - Top
    fields=re.split("[,\t]",line.rstrip())
    name_i = fields.index("SNP Name")
    samp_i = fields.index("Sample ID")
    alle_1 = fields.index("Allele1 - Top")
    alle_2 = fields.index("Allele2 - Top")
    lgenf = []
    for chrom in range(27):
        lgenf.append(open ("{}-{}.lgen".format(output,chr2chr[chrom]),"w"))
    for line in f:
        fields   = re.split("[,\t]",line.rstrip())
        snp_name = fields[name_i]
        chrom    = conv(array[fields[name_i]][0])
        if snp_name  not in array:
            print("Unknown SNP name in line "+line)
            continue
        a1       = fields[alle_1]
        a2       = fields[alle_2]
        entry = "{}{}{}{}{}{}{}{}{}{}".format(fields[samp_i],TAB,fields[samp_i],TAB,snp_name,TAB,a1,TAB,a2,EOL)
        lgenf[chrom].write(entry)
    for f in lgenf: f.close()


def outputMap(array,outname):
    entries = [[] for chrom in range(27) ]
    i=0
    for snp in array:
        curr = array[snp]
        data = curr[1:]
        data.append(snp)
        entries[curr[0]].append(data)
        i=i+1
    for chrom in range(27):
        mapf= open("{}-{}.map".format(outname,chr2chr[chrom]),"w")
        entries[chrom].sort()
        for [pos,cm,snp] in entries[chrom]:
            mapf.write("{}\\t{}\\t{}\\t{}\\n".format(chrom,snp,cm,pos))
        mapf.close()
            

args = parseArguments()

array = parseArray(args.array)
outputMap(array,args.output)

