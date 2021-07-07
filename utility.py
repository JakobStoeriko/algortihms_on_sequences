from Simon_tree import SimonTree
from s_connection import SConnection
from collections import deque
from tqdm import tqdm
import os
import sys
import re
from itertools import islice


def input_regex(path):
	cwd = os.getcwd()
	os.chdir(path)
	entries = os.listdir()
	for entry in entries:
		with open('temp.txt',"w") as temp_file, open(entry) as fasta:
			for line in fasta:
				if line[0] != '>':
					line = re.findall(r'[ACGT]', line)
					if not line:
						line.append('>')
					line.append("\n")
				data = "".join(str(x) for x in line)
				temp_file.write(data)
			os.rename(r'temp.txt', r''+entry)
	os.chdir(cwd)

def split_genes(path):
	cwd = os.getcwd()
	os.chdir(path)
	with open(os.path.basename(path)+'.len') as table:
		for line in table:
			if line[0] != '#':
				line = line.split()
				newpath = os.path.dirname(os.path.dirname(path)) +'/preprocessed_data/'+ line[0]
				if not os.path.exists(newpath):
					os.mkdir(newpath)
				with open(newpath +'/'+ line[0] + '.fasta','w') as out, open(os.path.basename(path)+'.fasta') as fasta:
					for line1,line2 in zip(fasta,fasta):
						out.write(line1)
						out.write(line2[int(line[1])-1:int(line[2])]+'\n')
				
				



def transform_input(w):
	alphlist = sorted(list(set(w)),key=str.lower)
	indexlist = [i for i in range(1,len(set(w))+1)]

	w_dict = {letter:rank for (letter,rank) in zip(alphlist,indexlist)}
	for c in set(w):
		w = w.replace(c,str(w_dict[c]))
		
	return w
