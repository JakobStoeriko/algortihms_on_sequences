from collections import deque
import numpy as np
from utility import transform_input


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
	
class SimonNode:
	"""
	A node-class used to represent nodes of Simon-Trees
	
	Attributes
	----------
	start : int
		Starting index of the associated k-block
	end : int
		Ending intex of the associated k-block
	parent : SimonNode
		Parent Node of this Node. Can be None
	children : deque
		A deque in which references to the children of this Node are 
		stored.
	connect : SimonNode
		The SimonNode to which this node is s-connected. This is only 
		used for computational purposes and should not be used as 
		reference. Specifically this may point to nodes whose trees do 
		not exist anymore.
	visible : boolean
		Specifies if this node should be displayed when the tree is 
		visualized. The default value is True.	
	"""
	def __init__(self,start,end, parent,visibile=True):
		"""
		Parameters
		----------
		start : int
			Starting index of the associated k-block
		end : int
			Ending intex of the associated k-block
		parent : SimonNode
			Parent Node of this Node. Can be None
		visible : boolean
			Specifies if this node should be displayed when the tree 
			is visualized. The default value is True.
		"""
		self.start = start
		self.end = end
		self.parent = parent
		self.children = deque()
		self.connect = None
		self.visibile = visibile
		
	def __str__(self):
		return str(self.start) + "-" + str(self.end) 

class SimonTree:
	"""
	A class used to represent a Simon-Tree
	
	Attributes
	----------
	w : str
		The word to which the tree is associated
	root : SimonNode
		The root of the tree
	X : ndarray
		An array in which for every position, the next position where 
		the same character occurs is stored
	nodelist : list
		A list in which for every level a list with the nodes on that level are stored.
	
	Methods
	-------
	__findNode(i,p)
		Finds the leftmost node in which the character w[i] occurs on a non-ending 
		position
	__splitNode(i,a)
		Adds the new node [?:i] to the tree on the correct level
	"""
	def __init__(self,w):
		"""
		Parameters
		----------
		w : str
			The word to which the tree is associated
		"""
		self.w = w
		n = len(w)
		#add help-letter
		w += '$'
		self.X = next(w)
		self.root = SimonNode(n+1,n+1,self)
		p = self.root #always points to the Node which was last inserted
		#build tree
		for i in range(n,0,-1):
			a = self.__findNode(i,p)
			p = self.__splitNode(i,a)
		p = self.root
		#close open blocks appearing on leftmost branch	
		while True:
			p.start = 1
			if p.children:
				p = p.children[-1]
			else:
				break
		p = self.root
		#remove help-letter and associated block. 
		w = w[:-1]
		self.root.children.popleft()
		#edit endpoints of nodes on rightmost branch to match removed help-letter
		while True:
			p.end = n
			if p.children:
				p = p.children[0]
			else:
				break
		self.nodelist = self.build_nodelist()
		
	def __findNode(self,i,p):
		"""
		Determines the Node of which the new node associated to position 
		i will be the child.
		After calling this method one should call __splitNode(i,a) with 
		a being the output of this method to insert the node into the 
		tree at the correct position.
		
 		Parameters
		----------
		i : int
			index which shall be inserted into the tree
		p : SimonNode
			Pointer to the last inserted node
		
		Returns
		-------
		p - parent node of new node associated to position i.
		"""
		while p != self.root:
			r = p.end
			r_p = p.parent.end
			if self.X[i-1] >= r and self.X[i-1] < r_p:
				return p
			else:
				p.start = i+1
				p = p.parent
		return p
	
	def __splitNode(self,i,a):
		"""
		Appends a new node, associated with position i, to the tree.
		This method should only ever be called directly after calling 
		__findNode(i,p) and a should be the output of said call.
		
		Parameters
		----------
		
		"""
		r = a
		while r != self.root:
			if r != r.parent.children[-1]:
				break
			r = r.parent
		if r == self.root and not a.children:
			a.start = 0
			a.end = i+1
			a.children.append(SimonNode(i+1,i+1,a))
			a.children.append(SimonNode(0,i,a))
		else:
			a.children.append(SimonNode(0,i,a))
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
		dq.append((self.root,0))
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
				if T[i][j].visible:
					print(i,T[i][j], sep = ";", end = '		')
			print("\n")

