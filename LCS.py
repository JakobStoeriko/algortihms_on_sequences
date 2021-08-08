import numpy as np

def LCS(X,Y):
	"""
	Computes the length of the longest common subsequence of input words X 
	and Y. This method implements a dynamic programming algorithm with a 
	runtime of O(n*m) where n and m are the wordlengths of X and Y 
	respectively.
	
	Parameters
	----------
	X : str
		first input word
	Y : str
		second input word
		
	Returns
	-------
	lcs : the lenght of the longest common subsequence of X and Y
	"""
	m = len(X)
	n = len(Y)
	C = np.zeros((m,n))
	for i in range(1,m):
		for j in range(1,n):
			if X[i-1] == Y[j-1]:
				C[i,j] = C[i-1,j-1]+1
			else:
				C[i,j] = max(C[i,j-1], C[i-1,j])
	lcs = C[m-1,n-1]
	return lcs
