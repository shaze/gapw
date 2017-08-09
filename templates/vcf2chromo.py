#! /usr/bin/env python3

import vcf
import sys
from numpy import empty, array

if len(sys.argv)==1:
    sys.argv = ["vcf2chromo.py", "$input", "$output"]

EOL=chr(10)
vcfname = sys.argv[1]
out     = sys.argv[2]


def getHaplos(v_r,outf,haplos):
    snp_i=0
    for rec in v_r:
       outf.write(" %d"%rec.POS)
       if not rec.is_snp: continue
       alleles=rec.alleles
       for sample_i, sample in enumerate(rec.samples):
           for h in [0,1]:
              haplos[sample_i,h,snp_i]=ord(sample.gt_bases[-h])
       snp_i=snp_i+1
    outf.write(EOL)


def outputHaplos(outf,haplos):
   (num_samples,numh,num_snps)=haplos.shape
   for sample in range(num_samples):
      for h in range(numh):
         for snp in range(num_snps):
             outf.write("%s"%chr(haplos[sample,h,snp]))
         outf.write(EOL)


               

def getDetails(vcfname,outf):
   v_r = vcf.Reader(filename=vcfname,compressed=True)
   sample_ids  = v_r.samples
   num_samples = len(sample_ids)
   num_snps=1
   for x in v_r:
       num_snps=num_snps+1
   outf.write("%d%s%d%sP"%(num_samples*2,EOL,num_snps,EOL))
   v_r = vcf.Reader(filename=vcfname,compressed=True)
   haplos=empty([num_samples,2,num_snps],'B')   
   getHaplos(v_r,outf,haplos)
   outputHaplos(outf,haplos)
   return (sample_ids,num_samples, num_snps)

   
outf = open(out,"w")
(sample_ids,num_samples,num_snps)=getDetails(vcfname,outf)
outf.close()

