from collections import deque
from tqdm import tqdm
import os
import sys
import re
from itertools import islice
import numpy as np


def input_regex(path):
	"""
	Takes files in fasta-format and trims the data to only contain "ACGT"
	
	Parameters
	----------
	path : str
		path to the directory containing the files to be trimmed
	"""
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
	"""
	Splits the file in fasta-format in the specified directory according to 
	a table which must be in the same directory. For this method to produce 
	meaningful data the fasta-file should be an alignment. 
	The resulting data will be stored in separate directories
	
	Parameters
	----------
	path : str
		path to the input directory
	"""
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
	"""
	Computes a dictionary which maps the characters of the input word to
	1...n where n is the alphabet size
	
	Parameters
	----------
	w : str
		the input word
	
	Returns
	-------
	w_dic : {}
		dictionary mapping the letters of the input word to 1...n
		The letters are sorted beforehand, such that the 
		lexicographically smallest letter is mapped to 1 and the
		lexicographically largest to n
	"""
	alphlist = sorted(list(set(w)),key=str.lower)
	indexlist = [i for i in range(1,len(set(w))+1)]

	w_dict = {letter:rank for (letter,rank) in zip(alphlist,indexlist)}
		
	return w_dict
	
	
	
def next(w):
	"""Calculates an array in that for each position of the input word, the 
	next position where the same character occurs is stored.
	
	Parameters
	----------
	w : str
		The input word
		
	Returns
	-------
	next : np.ndarray
		Array in which for every position the next position where that 
		same character occurs is stored. If the character doesn't occur 
		anymore inside w, 0 is stored.
	"""
	w_dic = transform_input(w)
	k = len(set(w))
	next = np.zeros(len(w))
	#help array to store for each character on which position it occured last
	temp = np.ones(k)*(len(w)+1)
	#Run backwards through the word. Update the output array using the help array, then
	#update the help array to store the new last occurence of that character
	for i in range(len(w),0,-1):
		next[i-1] = temp[w_dic[w[i-1]]-1]
		temp[w_dic[w[i-1]]-1] = i
	return next
	
	
def last(w):
	"""Calculates an array in that for each position of the input word, the 
	previous position where the same character occurs is stored.
	
	Parameters
	----------
	w : str
		The input word
		
	Returns
	-------
	next : np.ndarray
		Array in which for every position the previous position where that 
		same character occurs is stored. If the character doesn't occur 
		anymore inside w, 0 is stored.
	"""
	w_dic = transform_input(w)
	k = len(set(w))
	last = np.zeros(len(w))
	temp = np.zeros(k)
	for i in range(len(w)):
		last[i] = temp[w_dic[w[i]]-1]
		temp[w_dic[w[i]]-1] = i+1
	return last
