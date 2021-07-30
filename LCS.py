import numpy as np

def LCS(X,Y):
	m = len(X)
	n = len(Y)
	C = np.zeros((m,n))
	for i in range(1,m):
		for j in range(1,n):
			if X[i-1] == Y[j-1]:
				C[i,j] = C[i-1,j-1]+1
			else:
				C[i,j] = max(C[i,j-1], C[i-1,j])
	return C[m-1,n-1]
