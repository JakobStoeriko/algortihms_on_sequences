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
	os.chdir(old_cwd+'/compare')
	Tree1.render(os.path.basename(path1)+'.png')
	Tree2.render(os.path.basename(path2)+'_correct.png')	
	return tree1.compare_rfd(tree2)
	

def generate_output(treelist,filename,dest_path,print_div_word,lev,correct_check,lcs):
	sys.setrecursionlimit(recursionlimit)
	old_cwd = os.getcwd()
	os.chdir(dest_path)
	
	n = len(treelist)
	t_dm = np.full([n,n],np.nan)
	if lev:
		levenshtein_dm = np.full([n,n],np.nan)
		lev_max = 0
		lev_min = np.nan
	if lcs:
		lcs_dm = np.full([n,n],np.nan)
		lcs_max = 0
		lcs_min = np.nan
	namelist = []
	i = 0
	maximum = 0
	minimum = np.nan
	average = 0
	m = (len(treelist)-1)*len(treelist)/2
	with open("{a}.txt".format(a=filename), 'w') as output:
		while treelist:
			entry_w,W = treelist.pop()
			n = len(treelist)
			for j in range(n):
				entry_v,V = treelist[n-j-1]
				SC = SConnection(W,V)
				simk = SC.max_simk()
				
				###calculate upper right triangle of distance matrix
				t_dm[i][i+j+1] = simk
				t_dm[i+j+1][i] = simk
				if lev:
					ld = edit_distance(W.w,V.w)
					levenshtein_dm[i][i+j+1] = ld
					levenshtein_dm[i+j+1][i] = ld
					lev_max = max(ld,lev_max)
					lev_min = min(ld,lev_min)
				if lcs:
					lcs = LCS(W.w,V.w)
					lcs_dm[i][i+j+1] = lcs
					lcs_dm[i+j+1][i] = lcs
					lcs_max = max(lcs,lcs_max)
					lcs_min = min(lcs,lcs_min)
					
				maximum = max(simk,maximum)
				minimum = min(simk, minimum)
				###direct compare
				average += simk
				if correct_check and max_sim_k_binary_search(W.w,V.w) != simk:
					sys.exit('Implementation falsch')
				output.write(entry_w+','+entry_v+','+str(simk) + (', div_word: '+ SC.build_div_word() if print_div_word else '') + '\n')
				del SC,V
			del W
				
			#### distance matrix
			i+=1
			namelist.append(entry_w)

		###direct compare
		average /=m
		output.write("average: " + str(average))
		
	###normalise and expand distance matrix
	t_dm = np.nan_to_num(t_dm,nan=maximum)
	#t_dm = 1 - (t_dm-minimum)/(maximum-minimum)
	t_dm = 1-t_dm/maximum
	if lev:
		levenshtein_dm = np.nan_to_num(levenshtein_dm,nan=lev_max)
		levenshtein_dm = (levenshtein_dm-lev_min)/(lev_max-lev_min)
		with open('distance_compare_lev.txt','w') as distance_compare:
			for i in range(1,len(t_dm)):
				distance_compare.write(namelist[i]+','+str(t_dm[0][i])+','+str(levenshtein_dm[0][i])+'\n')
	if lcs:
		lcs_dm = 1 - (np.nan_to_num(lcs_dm,nan=lcs_max)-lcs_min)/(lcs_max-lcs_min)
		with open('distance_compare_lcs.txt','w') as distance_compare:
			for i in range(1,len(t_dm)):
				distance_compare.write(namelist[i]+','+str(t_dm[0][i])+','+str(lcs_dm[0][i])+'\n')
			
	###print distance matrix:
	np.savetxt('distance_matrix.txt',t_dm,delimiter=',')
				
	
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
	
	
def generate_average(dest_path,treelist,filename,print_div_word):
	sys.setrecursionlimit(recursionlimit)
	old_cwd = os.getcwd()
	os.chdir(dest_path)
	average = 0
	n = (len(treelist)-1)*len(treelist)/2
	with open("{a}.txt".format(a=filename), 'w') as output:
		while treelist:
			entry_w,W = treelist.pop()
			for j in range(len(treelist)):
				entry_v,V = treelist[j]
				SC = SConnection(W,V)
				max_simk = SC.max_simk()
				average += max_simk
				output.write(entry_w+','+entry_v+','+str(max_simk) + (', div_word: '+ SC.build_div_word() if print_div_word else '') + '\n')
		average/=n
		output.write("average: " + str(average))
	os.chdir(old_cwd)	
		
	
	
def generate_random_fasta(letters,n,m,dest_path):
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


	
def generate_treelist_from_fasta(input_path, dest_path):
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
				if line[0] == '>' and len(line) == 1:
					continue
				elif line[0] == '>':
					if name != '' and v != '':
						treelist.append((name,SimonTree(v).extend()))
						v = ''
					name = line[1:-1]
				else:
					v += line.rstrip('\n')
			if name != '' and v != '':
				treelist.append((name,SimonTree(v).extend()))
	os.chdir(old_cwd)
	return treelist
	
