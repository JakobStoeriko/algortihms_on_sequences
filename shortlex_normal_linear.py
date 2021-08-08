import numpy as np
import math
from sorting_techniques import pysort
from utility import transform_input
from operator import itemgetter
from utility import next
from utility import last

def calc_xcoordinates(w):
	"""
	Calculates the x-coordinates of the input word. The x-coordinate of a 
	position is the length of the shortest X-Ranker that can reach said 
	position
	
	Parameters
	----------
	w : str
		the input word
		
	Returns
	-------
	x : ndarray
		array storing for each position the corresponding x-coordinate
	"""
	l = last(w)
	L = [0]
	x = np.zeros(len(w))
	for i in range(1,len(w)+1):
		if l[i-1] == 0:
			x[i-1] = 1
			L.clear()
			L.append(0)
		else:
			for j in reversed(L):
				if j<l[i-1]:
					x[i-1] = x[i_j-1]+1
					L = [k for k in L if k<=i_j]
					break
				i_j = j
		L.append(i)
	return x

def calc_ycoordinates(w,k,x):
	"""
	Calculates the y-coordinates of the input word. The y-coordinate of a 
	position is the length of the shortest Y-Ranker that can reach said 
	position. If for a position i and a position j which is the greatest 
	position left of i which can be reached by a ranker of minimal length
	x_i + y_j > k+1, y_i is set to infinity and thereby marked for 
	deletion
 
	Parameters
	----------
	w : str
		the input word
	k : int
		k for which sim-k-equivalence is to be tested
	x : []
		x-coordinates of w
		
	Returns
	-------
	x : ndarray
		array storing for each position the corresponding y-coordinate
		or infinity if the position is marked for deletion
	"""
	n = next(w)
	L = [len(w)+1]
	y = np.zeros(len(w))
	for i in range(len(w),0,-1):
		if n[i-1] == len(w)+1:
			if x[i-1]+1 > k+1:
				y[i-1] = np.inf
				n = [p if p!=i else n[i-1] for p in n]
			else:
				y[i-1] = 1
				L.clear()
				L.append(i)
				L.append(len(w)+1)
		else:
			for j in L:
				if j > n[i-1]:
					if x[i-1] + y[i_j-1]+1 > k+1:
						y[i-1] = np.inf
						n = [p if p!=i else n[i-1] for p in n]
					else:
						y[i-1] = y[i_j-1]+1
						L = [i]+[k for k in L if k>=i_j]
					break
				i_j = j
	return y
	
def prune_w(w,x,y):
	"""
	Deletes all positions i from w where y_i is infinity
	
	Parameters
	----------
	w : str
		the input word
	x : []
		x-coordinates of w
	y : []
		y-coordinates of w
		
	Returns
	-------
	res : str
		the pruned word
	x_new : []
		pruned x-coordinates
	y_new : []
		pruned y-coordinates
	"""
	x_new = []
	y_new = []
	res= ""
	for i in range(len(y)):
		if not math.isinf(y[i]):
			x_new.append(int(x[i]))
			y_new.append(int(y[i]))
			res += w[i]
	return res,x_new,y_new
	
def build_blocks(w,x,y,k):
	"""
	Builds blocks to partition the input word. Blocks with an odd index
	contain positions which can be resorted without changing the sim-k-class
	Blocks with an even index contain positions which cannot be swapped.
	Blocks can be empty.
	
	Parameters
	----------
	w : str 
		the input word
	x : []
		x-coordinates of w
	y : []
		y-coordinates of w
	k : int
		k for which sim-k-equivalence is to be tested
	
	Returns
	-------
	L : [[]]
		list of blocks. Blocks with even index contain positions which 
		must remain in order, blocks with odd index contain positions
		which can be resorted without changing sim-k-class
	i : int
		number of blocks which can be reordered
	"""
	L = []
	L.append([])
	i = 1
	if x[0]+y[0] == k+1:
		i=2
		L.append([])
	L[i-1].append(0)
	for j in range(1,len(w)):
		if x[j]+y[j] == k+1:
			if i%2 == 1:
				i+=1
			else:
				if x[j] != x[j-1] or y[j] != y[j-1]:
					i += 2
					L.append([])
		else:
			if i%2 == 0:
				i+=1
		if i-1 == len(L):
			L.append([])
		L[i-1].append(j)
	if i%2 == 0:
		i = int(i/2)
		L.append([])
	else:
		i = int((i-1)/2)
	return L,i
	
	
def build_U(L,w,t):
	"""
	Builds a list of triples. For each block with odd index in L all 
	positions of this block is considered. The triples contain the 
	block-index, the letter in w corresponding to the position and the
	position itself. This list is then sorted via radix-sort.
	This sorting retains the order of the blocks and inside the blocks, 
	sorts all positions lexicographically while preserving the order of 
	positions where the same letter occurs.
	
	Parameters
	----------
	L : []
		list of blocks containing all positions of w. Positions which
		can be reordered must be in blocks with odd index, those who
		musn't be reordered in blocks with even index. The method 
		build_blocks() produces such a list
	w : str
		the input word
	t : int
		number of blocks which can be reordered
	
	Returns
	-------
	U : []
		radix-sorted list containing triples of block-index, letter and 
		position
	"""
	U = []
	for i in range(1,t+1):
		for j in L[2*i-1]:
			U.append((i,w[j],j))
	U.sort(key=itemgetter(0,1,2))		
	return U
	
def build_Ut(U,t):
	"""
	Builds a list of lists where each list corresponds to one of the odd 
	index blocks.
	
	Parameters
	----------
	U : []
		list containing triples as produced by build_U()
	t : int
		number of odd index blocks
		
	Returns
	-------
	Ut : []
		list of lists, each containing the letters of the triple of 
		corresponding blocks
	"""
	Ut = []
	for i in range(1,t+1):
		Ut.append([k[1] for k in U if k[0] == i])
	return Ut


def build_shortlex(L,Ut,w):
	"""
	Builds the shortlex-normalform of w from L and Ut. For even block 
	indices the original order as stored in L is used, for odd block 
	indices the newly sorted order as stored in Ut is used.
	
	Parameters
	----------
	L : [[]]
		list of lists containing blocks of w. Even index blocks contain 
		positions which must remain in order. Odd index blocks contain
		positions which must be reordered
	Ut : [[]]
		list of lists containing sorted odd index blocks of w.
	w : str
		the input word
		
	Returns
	-------
	shortlex : str
		the shortlex normalform of w
	"""
	shortlex = ""
	for t in range(len(L)):
		if t%2 == 0:
			for l in L[t]:
				shortlex += w[l]
		else:
			for u in Ut[int((t-1)/2)]:
				shortlex += u
	return shortlex
	
	
def shortlex_normalform(w,k):
	"""
	Builds the shortlex-normalform of w for sim-k index k.
	
	Parameters
	----------
	w : str
		the input word
	k : int
		sim-k index
	
	Returns
	-------
	shortlex : str
		the shortlex-normalform of w for k
	"""
	x = calc_xcoordinates(w)
	y = calc_ycoordinates(w,k,x)
	w,x,y = prune_w(w,x,y)
	L,t = build_blocks(w,x,y,k)
	U = build_U(L,w,t)
	Ut = build_Ut(U,t)
	shortlex = build_shortlex(L,Ut,w)
	return shortlex
	
def max_sim_k_binary_search(u,w):
	"""
	Computes the result of MAXSIMK for u and w via binary searching for k.
	k is computed via construction of shortlex-normalforms and checking for
	equality
	
	Parameters
	----------
	u : str
		first input word
	w : str
		second input word
		
	Returns
	-------
	high : MAXSIMK(u,w)
	"""
	low = 0
	high = min(len(u),len(w))-1
	mid = 0
	while low <= high:
		mid = int((high+low)/2)
		s_u = shortlex_normalform(u,mid)
		s_w = shortlex_normalform(w,mid)
		if s_u == s_w:
			low = mid+1
		else:
			high = mid-1
	return high

