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

def compare_newick_trees(path1,path2):
	old_cwd = os.getcwd()
	os.chdir(path1)
	with open('{a}.newick'.format(a=path1+os.path.basename(path1))) as nt1:
		tree1 = TreeNode.read(nt1.readlines())
	os.chdir(path2)
	with open('{a}.newick'.format(a=path2+os.path.basename(path2))) as nt2:
		tree2 = TreeNode.read(nt2.readlines())
	os.chdir(old_cwd)
	return tree1.compare_rfd(tree2)
	

def generate_output(treelist,filename,dest_path,print_div_word):
	sys.setrecursionlimit(100000)
	old_cwd = os.getcwd()
	os.chdir(dest_path)
	
	n = len(treelist)
	t_dm = np.full([n,n],np.nan)
	#old_dm = np.zeros((n,n))
	namelist = []
	i = 0
	maximum = 0
	
	average = 0
	m = (len(treelist)-1)*len(treelist)/2
	with open("{a}.txt".format(a=filename), 'w') as output, open("correct.txt",'w') as correct:
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
				#old_dm[i][i+j+1] =simk
				maximum = max(simk,maximum)
				
				###direct compare
				average += simk
				#correct.write(str(simk) + ',' + str(max_sim_k_binary_search(W.w,V.w))+'\n')
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
	t_dm = 1 - t_dm/maximum
	#for i in range(n):
	#	for j in range(i+1,n):
	#		old_dm[i][j] = 1-(old_dm[i][j]/maximum)
	#		old_dm[j][i] = old_dm[i][j]
	#print(old_dm)
			
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
	#print('Robinson-Foulds-Distance:{a}'.format(a=compare_newick_trees(dest_path,'/preprocessed_data/{a}'.format(a=filename))))
	os.chdir(old_cwd)
	print('finished')
	
	
def generate_average(dest_path,treelist,filename,print_div_word):
	sys.setrecursionlimit(100000)
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
	sys.setrecursionlimit(100000)
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
	sys.setrecursionlimit(100000)
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
			treelist.append((name,SimonTree(v).extend()))
	os.chdir(old_cwd)
	return treelist
