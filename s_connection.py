from Simon_tree import SimonTree
from Simon_tree import SimonNode
from collections import deque
	
class SConnection:
	def __init__(self,T,S):
		self.T = T
		self.S = S
		self.S_Con = self.build_S_connection()
			

	def build_S_connection(self):
		S_Con = [[]]
		queue = deque()
		S_Con[0].append((self.T.root,self.S.root))
		self.T.root.connect = self.S.root
		self.S.root.connect = self.T.root
		t_nodelist = self.T.nodelist
		s_nodelist = self.S.nodelist
		for i,j in zip(self.T.root.children,self.S.root.children):
			if len(S_Con) <= 1:
				S_Con.append([])
			if set(self.T.w[i.end-1:]) == set(self.S.w[j.end-1:]):
				S_Con[1].append((i,j))
				i.connect = j
				j.connect = i
				for i,j in zip(i.children,j.children):
					queue.append((i,j,1))	
		while queue:
			flag = True
			(t_node,s_node,k) = queue.popleft()
			if len(self.T.w[t_node.end:])<k or len(self.S.w[s_node.end:])<k:
				continue
			unionset = set(self.T.w[t_node.end-1:]).union(set(self.S.w[s_node.end-1:]))
			for t in unionset:
				i = self.T.w[t_node.end-1:].find(t)+t_node.end+1
				j = self.S.w[s_node.end-1:].find(t)+s_node.end+1
				if i>len(self.T.w) or j>len(self.S.w):
					flag = False
					break
				for l in range(len(t_nodelist[k])-1,-1,-1):
					x = t_nodelist[k][l]
					if i >= x.start:
						break
				if x.end < i:
					flag = False
					break
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
	
	def build_div_word():
		pass
		
	def max_simk(self):
		for i,j in zip(range(len(self.T.nodelist)),range(len(self.S.nodelist))):
			if len(self.S_Con) <= i or len(self.S_Con) <= j:
				return i-1
			if not self.S_Con[i] or (self.T.nodelist[i][0],self.S.nodelist[j][0]) != self.S_Con[i][-1]:
				return i-1
		return i
