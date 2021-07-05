from collections import deque
import numpy as np

def next(w):
	k = len(set(w))
	next = np.zeros(len(w))
	temp = np.ones(k)*(len(w)+1)
	for i in range(len(w),0,-1):
		next[i-1] = temp[int(w[i-1])-1]
		temp[int(w[i-1])-1] = i
	return next
	
class SimonNode:
	def __init__(self,start,end, parent,visability):
		self.start = start
		self.end = end
		self.parent = parent
		self.children = deque()
		self.visability = visability
		self.connect = None
		
	def __str__(self):
		return str(self.start) + "-" + str(self.end) 

class SimonTree:
	def __init__(self,w):
		self.w = w
		n = len(w)
		w = w + str(len(set(w))+1)
		self.X = next(w)
		self.root = SimonNode(n+1,n+1,self,True)
		p = self.root
		for i in range(n,0,-1):
			a = self.findNode(i,p)
			p = self.splitNode(i,a)
		p = self.root	
		while True:
			p.start = 1
			if p.children:
				p = p.children[-1]
			else:
				break
		p = self.root
		self.root.children.popleft()		
		while True:
			p.end = n
			if p.children:
				p = p.children[0]
			else:
				break
		self.nodelist = self.build_nodelist()
		
	def findNode(self,i,p):
		while p != self.root:
			r = p.end
			r_p = p.parent.end
			if self.X[i-1] >= r and self.X[i-1] < r_p:
				return p
			else:
				p.start = i+1
				p = p.parent
		return p
	
	def splitNode(self,i,a):
		r = a
		while r != self.root:
			if r != r.parent.children[-1]:
				break
			r = r.parent
		if r == self.root and not a.children:
			a.start = 0
			a.end = i+1
			a.children.append(SimonNode(i+1,i+1,a,True))
			a.children.append(SimonNode(0,i,a,True))
		else:
			a.children.append(SimonNode(0,i,a,True))
		return a.children[-1]
		
	def extend(self):
		t = self.nodelist
		for i in range(len(t)):
			for j in range(len(t[i])):
				if not t[i][j].children:
					t[i][j].children.append(SimonNode(t[i][j].start,t[i][j].end,t[i][j],False))
		self.nodelist = self.build_nodelist()
		return self
	
	
	def build_nodelist(self):
		T = [[]]
		dq = deque()
		dq. append((self.root,0))
		while dq:
			node,k = dq.popleft()
			if len(T) <= k:
				T.append([])
			T[k].append(node)
			for i in range(len(node.children)-1,-1,-1):
				dq.append((node.children[i],k+1))
		return T
		
	def visualize(self):
		T = self.nodelist
		for i in range(len(T)):
			for j in range(len(T[i])):
				print(i,T[i][j], sep = ";", end = '		')
			print("\n")

