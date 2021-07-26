import numpy as np
import math
from sorting_techniques import pysort
from utility import transform_input
from operator import itemgetter

def last(w):
	k = len(set(w))
	last = np.zeros(len(w))
	temp = np.zeros(k)
	for i in range(len(w)):
		last[i] = temp[int(w[i])-1]
		temp[int(w[i])-1] = i+1
	return last
	
def next(w):
	k = len(set(w))
	next = np.zeros(len(w))
	temp = np.ones(k)*(len(w)+1)
	for i in range(len(w),0,-1):
		next[i-1] = temp[int(w[i-1])-1]
		temp[int(w[i-1])-1] = i
	return next

def calc_xcoordinates(w):
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
	
def build_blocks(w,x,y,k):
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
	U = []
	for i in range(1,t+1):
		for j in L[2*i-1]:
			U.append((i,w[j],j))
	return U
	
def build_Ut(U,t):
	Ut = []
	for i in range(1,t+1):
		Ut.append([k for k in U if k[0] == i])
	return Ut

def prune_w(w,x,y):
	x_new = []
	y_new = []
	res= ""
	for i in range(len(y)):
		if not math.isinf(y[i]):
			x_new.append(int(x[i]))
			y_new.append(int(y[i]))
			res += w[i]
	return res,x_new,y_new

def build_shortlex(L,Ut,w):
	shortlex = ""
	for t in range(len(L)):
		if t%2 == 0:
			for l in L[t]:
				shortlex += w[l]
		else:
			for u in Ut[int((t-1)/2)]:
				shortlex += u[1]
	return shortlex

def sort_U(U):
	Un = []
	dic = {}
	for u in U:
		s = int(str(u[0])+u[1]+str(u[2]))
		Un.append(s)
	sortObj = pysort.Sorting()
	sortObj.radixSort(Un)
	U = []
	for u in Un:
		s = str(u)
		U.append((int(s[0]),s[1],int(s[2])))		
	return U
	
	
def shortlex_normalform(w,k):
	x = calc_xcoordinates(w)
	y = calc_ycoordinates(w,k,x)
	w,x,y = prune_w(w,x,y)
	L,t = build_blocks(w,x,y,k)
	U = build_U(L,w,t)
	U.sort(key=itemgetter(0,1,2))
	#if(t!=0):
	#	U = sort_U(U)
	Ut = build_Ut(U,t)
	return build_shortlex(L,Ut,w)
	
def max_sim_k_binary_search(u,w):
	low = 0
	high = min(len(u),len(w))-1
	mid = 0
	u = transform_input(u)
	w = transform_input(w)
	while low <= high:
		mid = int((high+low)/2)
		s_u = shortlex_normalform(u,mid)
		s_w = shortlex_normalform(w,mid)
		if s_u == s_w:
			low = mid+1
		else:
			high = mid-1
	return high

