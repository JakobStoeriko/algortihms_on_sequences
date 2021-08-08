import utility
import maxsimk_framework
import os
import sys
from argparse import ArgumentParser

def create_output(path,name,div_word,trim,lev,correct_check,lcs):
	"""
	Wrapper function for maxsimk_framework.generate_treelist_from_fasta and 
	maxsimk_framework.generate_output.
	Sets pathnames and ensures folders are present.
	
	Attributes
	----------
	path : str
		path to working directory
	name : str
		directory name of fasta-files
	div_word : Bool
		if True, a minimal diverging word will be printed. Passed to 
		maxsimk_framework.generate_output
	trim : Bool
		if True, the input files will be trimmed to only contain the
		alphabet "ACGT". Used for processing DNA-sequences
	lev : Bool
		if True, the Levenshtein-distance will be calculated alongside
		the MAXSIMK-distance. Passed to 
		maxsimk_framework.generate_output
	lcs : Bool
		if True, the LCS-distance will be calculated alongside
		the MAXSIMK-distance. Passed to
		maxsimk_framework.generate_output
	correct_check : Bool
		if True, the MAXSIMK implementation will be checked for
		correctnes by comparing with an implementation based on 
		shortlex-normalforms. Passed to 
		maxsimk_framework.generate_output
	
	"""
	cwd = os.getcwd()
	os.chdir(path)
	foldername = 'results/'+ name
	if not os.path.exists(foldername):
		os.mkdir(foldername)
	input_path = path+'/preprocessed_data/' + name
	dest_path = path+'/'+foldername
		
	if trim:
		utility.input_regex(input_path)
		print('trim complete')	
		
	treelist = maxsimk_framework.generate_treelist_from_fasta(input_path)
	print('treelist built')
			
	maxsimk_framework.generate_output(treelist,name,dest_path,div_word,lev,correct_check,lcs)
	os.chdir(cwd)	
	

def main():
	"""
	Main Method of the framework. The method works on command line arguments
	
	Command line arguments
	----------------------
	path : str 
		path to working directory
	
	mutually exclusive
	------------------
	nt : str str
		Compare newick trees. Takes the path to the corresponding
		.newick files as arguments
	s : str
		Split genes from fasta. Takes the name of fasta-file to be split
		as argument
	cr : str int int
		Create a fasta-file filled with random strings. The first
		argument provides the alphabet, the second the wordlength and
		the third the number of strings constructed
	com
		Create output-files from fasta-files
		subcommands
		-----------
		-trim : Trims the input files to contain only "ACGT"
		-div_word : calculates a minimal diverging word between each wordpair
		-lev : calculates the levenshtein-distance alongside MAXSIMK
		-lcs : calculates the lcs-distance alongside MAXSIMK
		-correct : checks MAXSIMK-implementation for correctness
		
		s : str
			Process a single directory. The argument provides the 
			directory name
		a
			Process all directories in preprocessed_data
	"""
	parser = ArgumentParser()
	parser.add_argument('-path',default=os.path.dirname(os.getcwd()),help='path to working directory')
	subparsers = parser.add_subparsers(dest = 'subcommand')
	
	parser_compare = subparsers.add_parser('nt', help='Compare two newick trees')
	parser_compare.add_argument('path1',help='name of computed tree')
	parser_compare.add_argument('path2',help='name of phylogenetical tree')
	
	parser_split = subparsers.add_parser('s',help='Split genes from fasta')
	parser_split.add_argument('name',help='name of fasta to be split')
	
	parser_random = subparsers.add_parser('cr',help='Generate a fasta file of random strings')
	parser_random.add_argument('letters',help='Alphabet from which random strings are constructed')
	parser_random.add_argument('n',type=int,help='Number of Strings constructed')
	parser_random.add_argument('m',type=int,help='Length of constructed strings')
	
	parser_create = subparsers.add_parser('com',help='Create output files from fasta file')
	parser_create.add_argument('-trim',action='store_true', default = False,help='Trims the input file to contain only the alphabet ACGT. Intended for DNA-data only')
	parser_create.add_argument('-div_word',action='store_true',default=False,help='Prints a minimal diverging word for every pair of words')
	parser_create.add_argument('-lev',action='store_true',default=False,help='Computes the Levenshtein-Distance along with MAXSIMK')
	parser_create.add_argument('-correct',action='store_true',default=False,help='Checks for correctnes, by comparing the computation of MAXSIMK with another implementation based on shortlex-normalforms')
	parser_create.add_argument('-lcs',action='store_true',default=False,help='Computes the LCS along with MAXSIMK')
	
	subparsers_create = parser_create.add_subparsers(dest='subcommand_c')
	
	
	parser_single = subparsers_create.add_parser('s',help='Process a single fasta file')
	parser_single.add_argument('name',help='name of fasta file to be read, without extension')
	
	
	parser_all = subparsers_create.add_parser('a',help='Process all files in preprocessed_data directory')
	
	args = parser.parse_args()
	
	os.chdir(args.path)
	
	if args.subcommand == 'nt':
		path_1 = args.path+'/results/'+args.path1
		path_2 = args.path+'/phylogenetical trees/' +args.path2
		print(maxsimk_framework.compare_newick_trees(path_1,path_2))
	
	if args.subcommand == 's':
		path = args.path + '/data_raw/'+ args.name
		utility.split_genes(path)
	
	if args.subcommand == 'cr':
		input_path = args.path + '/preprocessed_data'
		if not os.path.exists(input_path):
			os.mkdir(input_path)
		maxsimk_framework.generate_random_fasta(args.letters,args.n,args.m,input_path)
		print('to use this data use the following format: name = r,s={d},c={a},l={b}'.format(a=args.n,b=args.m,d=len(args.letters)))
		
	if args.subcommand =='com':
		if not os.path.exists('results'):
				os.mkdir('results')
		if args.subcommand_c == 'a':
			entries = os.listdir('preprocessed_data')
			for entry in entries:
				print(entry)
				create_output(args.path,entry,args.div_word,args.trim,args.lev,args.correct,args.lcs)
			
		elif args.subcommand_c == 's':	
			create_output(args.path,args.name,args.div_word,args.trim,args.lev,args.correct,args.lcs)
		
if __name__ == '__main__':
	main()
