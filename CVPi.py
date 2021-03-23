import gzip, sys, os, fileinput, argparse, subprocess, glob
import time
from File_validation import validation
from Genome_alignmnet import alignment
from Variant_calling import Vcalling
tic = time.perf_counter()

path = os.getcwd();
parser = argparse.ArgumentParser(description='CVPi Pipeline for clnical variant analysis.')
parser.add_argument('-f','--fastq', help='Input file name',required=True)
parser.add_argument('-ref','--refgenome',help='Output file name', required=True)

args = parser.parse_args()
fastq_file = args.fastq
ref_file = args.refgenome

os.system(" export PATH=/usr/bin:/home/agct/.cargo/bin:/usr/local/bin ")

validation(fastq_file)

alignment(fastq_file,ref_file)

Vcalling(fastq_file,ref_file)

toc = time.perf_counter()

time_taken = (toc - tic)/60

print( "Time taken = " + str(time_taken))
output_file = fastq_file[0] + "_log.txt"
f = open( output_file, 'w')
sys.stdout = f
f.close()