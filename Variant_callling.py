import gzip, sys, os, fileinput, argparse, subprocess, glob, re
import time

def Vcalling(fastq_file,ref_file):
	print(fastq_file,ref_file)
	path = os.getcwd();
	fastq = fastq_file.split(".")
	print("-"*95 + "Calling Variants (longshot)" + "-"*95)

	os.system("longshot --bam  " + path + "/" + fastq[0] + ".aligned.sorted.bam  --ref  " + path + "/" + ref_file + "  --out "+  path + "/" + fastq[0] + ".vcf" )

	print("-"*95 + "END" + "-"*95)

	pass