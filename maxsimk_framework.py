from Simon_tree import SimonTree
from s_connection import SConnection
import string
import random
import sys
import os
from tqdm import tqdm
from collections import deque
from utility import transform_input
from scipy.spatial.distance import squareform
from skbio import DistanceMatrix
import numpy as np
from skbio.tree import nj
from skbio import TreeNode
from textwrap import fill
from shortlex_normal_linear import max_sim_k_binary_search
from nltk.metrics.distance import edit_distance
from LCS import LCS
from ete3 import Tree


recursionlimit = 10000

def compare_newick_trees(path1,path2):
	"""
	Computes the robinson-foulds-distance between two newick-trees, which
	are read from files at the specified location. Computes also a visual
	representation of the trees
	
	Parameters
	----------
	path1 : str
		path to the first .newick file
	path2 : str
		path to the second .newick file
	
	Returns
	-------
	rfd : float
		the robinson-foulds-distance between the trees
	"""
	old_cwd = os.getcwd()
	os.chdir(path1)
	path1 = path1+'/'+os.path.basename(path1)+'.newick'
	Tree1=Tree(path1)
	with open(path1) as nt1:
		tree1 = TreeNode.read(nt1.readlines())
	os.chdir(path2)
	path2 = path2+'/'+os.path.basename(path2)+'.newick'
	Tree2=Tree(path2)
	with open(path2) as nt2:
		tree2 = TreeNode.read(nt2.readlines())
	if not os.path.exists(old_cwd+'/compare'):
		os.mkdir(old_cwd+'/compare')
	os.chdir(old_cwd+'/compare')
	Tree1.render(os.path.basename(path1)+'.png')
	Tree2.render(os.path.basename(path2)+'_correct.png')	
	#return Tree1.robinson_foulds(Tree2)
	return tree1.compare_rfd(tree2)
	

def generate_output(treelist,filename,dest_path,print_div_word,lev,correct_check,lcs):
	"""
	Computes pairwise MAXSIMK and the MAXSIMK-distance between all
	SimonTrees in the treelist. The MAXSIMK-Values as well as a distance
	matrix is saved as .txt-file.
	Several optional calculations can be made.
	
	Parameters
	----------
	treelist : []
		list containing tuples consisting of a name and a SimonTree
	filename : str
		name of the output-file
	dest_path : str
		path to the destination folder
	print_div_word : Bool
		if True, a minimal diverging word will be printed
	lev : Bool
		if True, the Levenshtein-distance will be calculated alongside
		the MAXSIMK-distance. A distance matrix is saved as .txt-file
	lcs : Bool
		if True, the LCS-distance will be calculated alongside
		the MAXSIMK-distance. A distance matrix is saved as .txt-file
	correct_check : Bool
		if True, the MAXSIMK implementation will be checked for
		correctnes by comparing with an implementation based on 
		shortlex-normalforms
	"""
	sys.setrecursionlimit(recursionlimit)
	old_cwd = os.getcwd()
	os.chdir(dest_path)
	
	n = len(treelist)
	t_dm = np.zeros((n,n))
	if lev:
		levenshtein_dm = np.zeros((n,n))
	if lcs:
		lcs_dm = np.zeros((n,n))
	namelist = []
	i = 0
	average = 0
	m = (len(treelist)-1)*len(treelist)/2
	with open("{a}.txt".format(a=filename), 'w') as output:
		while treelist:
			entry_w,W = treelist.pop()
			n = len(treelist)
			for j in range(n):
				entry_v,V = treelist[n-j-1]
				SC = SConnection(W,V)
				maxsimk = SC.max_simk()
				# maxsimk can be maximal the length of the shorter
				# word
				n_maxsimk = 1 - maxsimk/min(len(W.w),len(V.w))
				
				# diagonal is always 0
				t_dm[i][i+j+1] = n_maxsimk
				t_dm[i+j+1][i] = n_maxsimk
				if lev:
					ld = edit_distance(W.w,V.w)
					levenshtein_dm[i][i+j+1] = ld
					levenshtein_dm[i+j+1][i] = ld
				if lcs:
					# lcs can be maximal the length of the 
					# longer word
					lcs = 1-LCS(W.w,V.w)/max(len(W.w),len(V.w))
					lcs_dm[i][i+j+1] = lcs
					lcs_dm[i+j+1][i] = lcs
					
				average += maxsimk
				
				if correct_check and max_sim_k_binary_search(W.w,V.w) != maxsimk:
					sys.exit('Implementation falsch')
				
				output.write(entry_w+','+entry_v+','+str(maxsimk) + (', div_word: '+ SC.build_div_word() if print_div_word else '') + '\n')
				
				#release objects not used anymore
				del SC,V
			del W
				
			
			i+=1
			namelist.append(entry_w)

		average /=m
		output.write("average: " + str(average))
		
			
	###print distance matrix:
	np.savetxt('distance_matrix.txt',t_dm,delimiter=',')
	
	if lev:
		np.savetxt('lev_dist_mat.txt',levenshtein_dm,delimiter=',')
		
	if lcs:
		np.savetxt('lcs_dist_mat.txt',lcs_dm,delimiter=',')
				
	
	###build newick tree		
	dm = DistanceMatrix(t_dm,namelist)
	#print(dm)
	tree = nj(dm)
	with open("{a}.tree".format(a=filename), 'w') as dest_file:
		dest_file.write(tree.ascii_art())
	tree = nj(dm, result_constructor=str)
	with open("{a}.newick".format(a=filename),'w') as newick_file:
		newick_file.write(tree)
	os.chdir(old_cwd)
	print('finished')
	
		
	
	
def generate_random_fasta(letters,n,m,dest_path):
	"""
	Generates a file in fasta-format filled with m randomized strings of
	length n over the alphabet letters and stores it at dest_path.
	
	Parameters
	----------
	letters : str
		Input alphabet
	n : int
		lenght of words
	m : int
		number of words
	dest_path : str
		path where the constructed file is stored
	"""
	sys.setrecursionlimit(recursionlimit)
	formatstring = 'r,s={d},c={a},l={b}'.format(a=n,b=m,d=len(letters))
	dest_path += '/'+formatstring
	if not os.path.exists(dest_path):
		os.mkdir(dest_path)
	old_cwd = os.getcwd()
	os.chdir(dest_path)
	with open(formatstring+'.fasta',"w") as fasta:
		for i in tqdm(range(n)):
			fasta.write('>{a}\n'.format(a=i))
			v = ''.join(random.choice(letters) for i in range(m))
			fasta.writelines(fill(v,80)+'\n')
	os.chdir(old_cwd)


	
def generate_treelist_from_fasta(input_path):
	"""
	Reads all files in fasta-format in the input_path and generates a list
	of tuples containing a name and the SimonTree associated to a word.
	A file can contain multiple words
	
	Parameters
	----------
	input_path : str
		path to the files
	
	Returns
	-------
	treelist : []
		a list containing tuples of names and SimonTrees
	"""
	sys.setrecursionlimit(recursionlimit)
	treelist = []
	old_cwd = os.getcwd()
	os.chdir(input_path)
	entries = os.listdir()
	for entry in tqdm(entries):
		with open(entry) as fasta:
			name = ''
			v = ''
			for line in fasta:
				# name missing
				if line[0] == '>' and len(line) == 1:
					continue
				# this is a header line containing the name
				elif line[0] == '>':
					# the previous word now ends. store it
					# only if its not empty
					if name != '' and v != '':
						treelist.append((name,SimonTree(v).extend()))
						v = ''
					name = line[1:-1]
				else:
					v += line.rstrip('\n')
			#store the last line
			if name != '' and v != '':
				treelist.append((name,SimonTree(v).extend()))
	os.chdir(old_cwd)
	return treelist
	
