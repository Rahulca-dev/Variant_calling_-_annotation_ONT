import gzip, sys, os, fileinput, argparse, subprocess, glob, pysam, re
import time

tic = time.perf_counter()



def alignment(fastq_file,ref_file):
	print(fastq_file,ref_file)
	path = os.getcwd();
	print(path)
	fastq = fastq_file.split(".")
	print("-"*95 + "Genome Alignment" + "-"*95)
	os.system("minimap2 -a " + ref_file + "  " + fastq[0] + "_trimmed.fastq  > " + fastq[0] + ".sam")
	sam_file = glob.glob(fastq[0] + '.sam')
	print(sam_file[0])
	# Generate unsorted BAM file
	out_bam = fastq[0] + ".bam"
	subprocess.call(["samtools", "view", "-bS", sam_file[0]],stdout=open(out_bam,'w'))
    # Generate sorted BAM file
	bam_file = glob.glob('*.bam')
	print(bam_file[0])
	pysam.sort("-o", path +"/" +fastq[0] + ".sorted.bam", bam_file[0])
	# Generate index for BAM file
	sorted_file = glob.glob('*.sorted.bam')
	print(sorted_file[0])
	pysam.index(sorted_file[0])
	print("-"*95 + "Genome Aligned" + "-"*95)



def Vcalling(fastq_file,ref_file):
	print(fastq_file,ref_file)
	path = os.getcwd();
	fastq = fastq_file.split(".")
	print("-"*95 + "Calling Variants (longshot)" + "-"*95)

	os.system("longshot --bam  " + fastq[0] + ".sorted.bam  --ref  " + ref_file + "  --out " + fastq[0] + ".vcf" )

	print("-"*95 + "END" + "-"*95)

	pass

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

def Annotation(Vcf_file,fastq_file):

	fastq = fastq_file.split(".")

	os.system("perl  convert2annovar.pl -format vcf4 " + vcf_file[0] + "  -outfile " + fastq[0] + ".avinput" )
	fastq = fastq_file.split(".")
	avinput_file = glob.glob(fastq[0] + '.avinput')
	os.system("perl table_annovar.pl " + avinput_file[0] + "  humandb/ -buildver hg19  -out "+ fastq[0] +"  -remove -protocol refGene,cytoBand,exac03,avsnp147,dbnsfp30a -operation gx,r,f,f,f -nastring . -csvout -polish  ")
	pass





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

fastq = fastq_file.split(".")
vcf_file = glob.glob(fastq[0] + '.vcf')
print(vcf_file[0])

Annotation(vcf_file,fastq_file)

toc = time.perf_counter()

time_taken = (toc - tic)/60

print( "Time taken = " + str(time_taken) + "mins")

