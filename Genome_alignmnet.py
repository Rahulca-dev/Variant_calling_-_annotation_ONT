import gzip, sys, os, fileinput, argparse, subprocess, glob, re
import time

def alignment(fastq_file,ref_file):
	print(fastq_file,ref_file)
	path = os.getcwd();
	fastq = fastq_file.split(".")
	print("-"*95 + "Genome Alignment" + "-"*95)
	os.system("minimap2 -a " + ref_file + " " + fastq[0] + "_trimmed.fastq  > " + fastq[0] + ".sam")
	sam_file = glob.glob(path + "/"+ fastq[0] + '.sam');
	print(sam_file)
	os.system("samtools view -S -b " + sam_file[0] + " > " + path + "/" + fastq[0] + ".bam")
	bam_file = glob.glob(path + "/"+ fastq[0] + '.bam');
	os.system("samtools sort -o  " + path + "/" + fastq[0] + ".aligned.sorted.bam  " + bam_file[0] )
	os.system("samtools index " + path + "/" + fastq[0] + ".aligned.sorted.bam  ")
	print("-"*95 + "Genome Aligned" + "-"*95)
	pass
