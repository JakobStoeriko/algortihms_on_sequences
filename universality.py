import numpy as np

def compute_universality_index(w):
	universality_index = 0
	count = len(set(w))
	C = np.zeros(count)
	
	for i in range(len(w)):
		if C[int(w[i])-1] == 0:
			C[int(w[i])-1] = 1
			count -= 1
		if count == 0:
			universality_index += 1
			count = len(set(w))
			C = np.zeros(count)
	return universality_index
