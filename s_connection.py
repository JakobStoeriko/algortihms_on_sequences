from Simon_tree import SimonTree
from Simon_tree import SimonNode
from collections import deque
	
class SConnection:
	"""
	A class for calculating the S-Connection between two SimonTrees.
	This connection can then be used to calculate MAXSIMK between the 
	corresponding words.
	
	Attributes
	----------
	T : SimonTree
		SimonTree associated to the first word
	S : SimonTree
		SimonTree associated to the second word
	S_Con : [[]]
		List of lists that contain for each level all the nodepairs that
		are in the S-Connection
		
	Methods
		-------
		build_S_connection
			Builds the S-Connection between the SimonTrees T and S
		build_div_word
			Builds a minimal diverging word between the two words
			associated with T and S
		max_sim_k
			Computes MAXSIMK between the words associated with T and 
			S
	"""
	def __init__(self,T,S):
		"""
		Paramteres
		----------
		T : SimonTree
			SimonTree associated to the first word
		S : SimonTree
			SimonTree associated to the second word
		"""
		self.T = T
		self.S = S
		self.S_Con = self.build_S_connection()
			

	def build_S_connection(self):
		"""
		Builds the S-Connection between the SimonTrees T and S.
		
		Returns
		-------
		S_Con : [[]]
			List of lists that contain for each level all the nodepairs that
			are in the S-Connection.
		"""
		S_Con = [[]]
		# emulate the p-connection by using a deque and doing a 
		# BFS-style traversal of the tree
		# only the children of connected nodes are added to the 
		# deque. These are exactly the nodes of the p-connection
		# which are possibly also in the s-connection.
		queue = deque()
		S_Con[0].append((self.T.root,self.S.root))
		self.T.root.connect = self.S.root
		self.S.root.connect = self.T.root
		t_nodelist = self.T.nodelist
		s_nodelist = self.S.nodelist
		#process first level
		for i,j in zip(self.T.root.children,self.S.root.children):
			if len(S_Con) <= 1:
				S_Con.append([])
			# two nodes of first level are in the s-connection if 
			# they have the same set of letters
			if set(self.T.w[i.end-1:]) == set(self.S.w[j.end-1:]):
				S_Con[1].append((i,j))
				i.connect = j
				j.connect = i
				for i,j in zip(i.children,j.children):
					queue.append((i,j,1))
		# BFS-style traversal	
		while queue:
			flag = True
			(t_node,s_node,k) = queue.popleft()
			if len(self.T.w[t_node.end:])<k or len(self.S.w[s_node.end:])<k:
				continue
			# consider a pair of nodes on level k+1
			# for every letter in the corresponding suffix it is
			# checked wether the nodes on level k, which correspond
			# to the next occurence of the letter occuring on
			# position i in the respective word,  are s-connected
			unionset = set(self.T.w[t_node.end-1:]).union(set(self.S.w[s_node.end-1:]))
			for t in unionset:
				#next occurence
				i = self.T.w[t_node.end-1:].find(t)+t_node.end+1
				j = self.S.w[s_node.end-1:].find(t)+s_node.end+1
				
				#letter doesnt occur anymore in the suffix
				if i>len(self.T.w) or j>len(self.S.w):
					flag = False
					break
					
				#find the corresponding node in T
				for l in range(len(t_nodelist[k])-1,-1,-1):
					x = t_nodelist[k][l]
					if i >= x.start:
						break
				if x.end < i:
					flag = False
					break
					
				#find the corresponding node in S
				for l in range(len(s_nodelist[k])-1,-1,-1):
					y = s_nodelist[k][l]
					if j >= y.start:
						break
				if y.end < j:
					flag = False
					break
					
				if x.connect != y or y.connect != x:
					flag = False
					break
			
			if flag:	
				if len(S_Con) <= k+1:
					S_Con.append([])
				S_Con[k+1].append((t_node,s_node))
				t_node.connect = s_node
				s_node.connect = t_node
				for i,j in zip(t_node.children,s_node.children):
					queue.append((i,j,k+1))
					
		return S_Con
	
	def build_div_word(self):
		"""
		Computes the lexicographicaly smallest minimal diverging word 
		between the words associated with the SimonTrees T and S.
		This method should only be called after build_S_connection() has
		been called. T
		he correctness of this method is only given, if the 
		SimonTrees have not been used in another instance of SConnection
		in the meantime.
		
		Returns
		-------
		w : str
			A lexicographically smallest minimal diverging word
			between the words associated with T and S
		"""
		w=''
		k=0
		# starting from the lowest nodepair on the leftmost branch which
		# is still s-connected
		while len(self.S_Con) > k and self.S_Con[k] and (self.T.nodelist[k][0],self.S.nodelist[k][0]) == self.S_Con[k][-1]:
			k+=1
		t_nodelist = self.T.nodelist
		s_nodelist = self.S.nodelist
		t_node = t_nodelist[k][0]
		s_node = s_nodelist[k][0]
		while k>0:
			# find the lexicographically smallest letter for which
			# the corresponding nodes on level k-1 are not
			# s-connected. Append this letter to the minimal
			# diverging word and continue from the nodepair on level
			# k-1
			unionset =  sorted(set(self.T.w[t_node.end-1:]).union(self.S.w[s_node.end-1:]))
			found = False
			#find next occurence
			for t in unionset:
				i = self.T.w[t_node.end-1:].find(t)+t_node.end+1
				j = self.S.w[s_node.end-1:].find(t)+s_node.end+1
				# letter t doesn't occur anymore in any one of the 
				# words. We have found a minimal diverging word
				# ending with t
				if i>len(self.T.w) or j>len(self.S.w):
					w += t
					return w
				
				# find corresponding node in T
				for l in range(len(t_nodelist[k-1])-1,-1,-1):
					x = t_nodelist[k-1][l]
					if i >= x.start:
						break
						
				# letter t doesn't occur anymore in one of the 
				# words. We have found a minimal diverging word
				# ending with t
				if x.end < i:
					w += t
					return w
				
				# find corresponding node in S
				for l in range(len(s_nodelist[k-1])-1,-1,-1):
					y = s_nodelist[k-1][l]
					if j >= y.start:
						break
						
				# letter t doesn't occur anymore in any one of the 
				# words. We have found a minimal diverging word
				# ending with t
				if y.end < j:
					w += t
					return w
					
				# if the nodes are not s-connected we add t to w
				# and update the nodes and k.	
				if x.connect != y or y.connect != x:
					w += t
					t_node = x
					s_node = y
					k -= 1
					found=True
					break
			# if no letter has been found to fullfill the condition
			# we end w
			if not found:
				return w
		return w
			
		
	def max_simk(self):
		"""
		Computes the result of MAXSIMK between the words associated with
		T and S. This is the level of the lowest nodepair on the
		leftmost branch of the S-Connection.
		
		Returns
		-------
		i : int
			MAXSIMK(w,v)
		"""
		for i,j in zip(range(len(self.T.nodelist)),range(len(self.S.nodelist))):
			if len(self.S_Con) <= i or len(self.S_Con) <= j:
				
				return i-1
			if not self.S_Con[i] or (self.T.nodelist[i][0],self.S.nodelist[j][0]) != self.S_Con[i][-1]:
				return i-1
		return i
