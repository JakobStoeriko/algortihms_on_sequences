import utility
import test
import os
import sys
from argparse import ArgumentParser

def create_output(path,name,div_word,trim,lev,correct_check,lcs):
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
		
	treelist = test.generate_treelist_from_fasta(input_path,dest_path)
	print('treelist built')
			
	test.generate_output(treelist,name,dest_path,div_word,lev,correct_check,lcs)
	os.chdir(cwd)	
	

def main():
	parser = ArgumentParser()
	parser.add_argument('-path',default=os.path.dirname(os.getcwd()),help='path to working directory')
	subparsers = parser.add_subparsers(dest = 'subcommand')
	
	parser_compare = subparsers.add_parser('nt', help='Compare computed newick tree to correct phylogenetical tree')
	parser_compare.add_argument('name',help='name of computed tree')
	parser_compare.add_argument('treename',help='name of phylogenetical tree')
	
	parser_split = subparsers.add_parser('s',help='Split genes from fasta')
	parser_split.add_argument('name',help='name of fasta to be split')
	
	parser_random = subparsers.add_parser('r',help='Generate a fasta file of random strings')
	parser_random.add_argument('letters',help='Alphabet from which random strings are constructed')
	parser_random.add_argument('n',type=int,help='Number of Strings constructed')
	parser_random.add_argument('m',type=int,help='Length of constructed strings')
	
	parser_create = subparsers.add_parser('c',help='Create output files from fasta file')
	parser_create.add_argument('-trim',action='store_true', default = False,help='Trims the input file to contain only the alphabet ACGT. Intended for DNA-data only')
	parser_create.add_argument('-div_word',action='store_true',default=False,help='Prints a minimal diverging word for every pair of words')
	#parser_create.add_argument('-com_nt', action='store', help='Compares the computed newick tree to the correct phylogenetical tree, which must be stored in the same folder as the input data')
	parser_create.add_argument('-lev',action='store_true',default=False,help='Computes the Levenshtein-Distance along with MAXSIMK')
	parser_create.add_argument('-correct',action='store_true',default=False,help='Checks for correctnes, by comparing the computation of MAXSIMK with another implementation based on shortlex-normalforms')
	parser_create.add_argument('-LCS',action='store_true',default=False,help='Computes the LCS along with MAXSIMK')
	
	subparsers_create = parser_create.add_subparsers(dest='subcommand_c')
	
	
	parser_single = subparsers_create.add_parser('s',help='Process a single fasta file')
	parser_single.add_argument('name',help='name of fasta file to be read, without extension')
	
	
	parser_all = subparsers_create.add_parser('a',help='Process all files in preprocessed_data directory')
	
	args = parser.parse_args()
	
	os.chdir(args.path)
	
	if args.subcommand == 'nt':
		path1 = args.path+'/results/'+args.name
		path2 = args.path+'/phylogenetical trees/' +args.treename
		print(test.compare_newick_trees(path1,path2))
	
	if args.subcommand == 's':
		path = args.path + '/data_raw/'+ args.name
		utility.split_genes(path)
	
	if args.subcommand == 'r':
		input_path = args.path + '/preprocessed_data'
		if not os.path.exists(input_path):
			os.mkdir(input_path)
		test.generate_random_fasta(args.letters,args.n,args.m,input_path)
		print('to use this data use the following format: name = r,s={d},c={a},l={b}'.format(a=args.n,b=args.m,d=len(args.letters)))
		
	if args.subcommand =='c':
		if not os.path.exists('results'):
				os.mkdir('results')
		if args.subcommand_c == 'a':
			entries = os.listdir('preprocessed_data')
			for entry in entries:
				print(entry)
				create_output(args.path,entry,args.div_word,args.trim,args.lev,args.correct,args.LCS)
			
		elif args.subcommand_c == 's':	
			create_output(args.path,args.name,args.div_word,args.trim,args.lev,args.correct,args.LCS)
		
if __name__ == '__main__':
	main()
