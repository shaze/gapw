

// First we convert from PLINK into ChromoPainter format
import java.nio.file.Paths;
import sun.nio.fs.UnixPath;


input  = params.input
indir   = params.indir



 Channel
   .fromFilePairs("${inpat}.{bed,bim,fam}",size:3, flat : true){ file -> file.baseName }  \
   .separate(all_bplink,bim,fam) { a -> [a,a[1],a[2]] }

process countInds {
     input:
       file(fam)
     output:
       file (numhaplos) into num_haplos_ch
     script:
          numhaplos = "nh.txt"
          template "count_haplotypes.py"
 }

process countSNPs {
  input:
     file (inp) from bim
  output:
    file  (out) into num_snps_ch
  script:
        out="num_snps.txt"

