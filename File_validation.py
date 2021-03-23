import gzip, sys, os, fileinput, argparse, subprocess, glob, re
import time

def validation(fastq_file):
	print (fastq_file)
	fastq = fastq_file.split(".")
	print("-"*95 + "Validation Protocol" + "-"*95)


	with open(fastq_file, "r") as f:
		read = f.readlines()
		count = 1;
		for line in read:
			if line == re.match("^@",line):
				count +=1;
			if count == 2:
				line = re.match("/(w+)/")
				count +=1;
			if count ==3:
				line = re.match("/+/")
				count +=1;
			if count ==4:
				line = re.match("/(w+)/")
		print("File validated")
	os.system("porechop -i " + fastq_file + " > " + fastq[0] + "_trimmed.fastq")
	print("-"*95 + "File Validated" + "-"*95)

	pass