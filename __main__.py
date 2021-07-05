import utility
import test
import os
import sys
from argparse import ArgumentParser

def create_output(path,name,div_word,trim):
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
			
	test.generate_output(treelist,name,dest_path,div_word)
	#test.generate_average(dest_path, treelist,name,div_word)
	os.chdir(cwd)	
	

def main():
	parser = ArgumentParser()
	parser.add_argument('-path',default=os.path.dirname(os.getcwd()),help='path to working directory')
	subparsers = parser.add_subparsers(dest = 'subcommand')
	
	parser_split = subparsers.add_parser('s',help='Split genes from fasta')
	parser_split.add_argument('name',help='name of fasta to be split')
	
	parser_random = subparsers.add_parser('r',help='Generate a fasta file of random strings')
	parser_random.add_argument('letters',help='Alphabet from which random strings are constructed')
	parser_random.add_argument('n',type=int,help='Number of Strings constructed')
	parser_random.add_argument('m',type=int,help='Length of constructed strings')
	
	parser_create = subparsers.add_parser('c',help='Create output files from fasta file')
	parser_create.add_argument('-trim',action='store_true', default = False,help='If this option is set, the input file will be trimmed to contain only the alphabet ACGT. Intended for DNA-data only')
	parser_create.add_argument('-div_word',action='store_true',default=False,help='If this option is set, a minimal diverging word will be printed')
	subparsers_create = parser_create.add_subparsers(dest='subcommand_c')
	
	
	parser_single = subparsers_create.add_parser('s',help='Process a single fasta file')
	parser_single.add_argument('name',help='name of fasta file to be read, without extension')
	
	parser_all = subparsers_create.add_parser('a',help='Process all files in preprocessed_data directory')
	
	args = parser.parse_args()
	
	os.chdir(args.path)
	
	if args.subcommand == 's':
		path = args.path + '/data_raw/'+ args.name
		utility.split_genes(path)
	
	if args.subcommand == 'r':
		input_path = args.path + '/preprocessed_data'
		if not os.path.exists(input_path):
			os.mkdir(input_path)
		test.generate_random_fasta(args.letters,args.n,args.m,input_path)
		print('to use this data use the following format: name = r,c={a},l={b}'.format(a=args.n,b=args.m))
		
	if args.subcommand =='c':
		if not os.path.exists('results'):
				os.mkdir('results')
		if args.subcommand_c == 'a':
			entries = os.listdir('preprocessed_data')
			for entry in entries:
				create_output(args.path,entry,args.div_word,args.trim)
			
		elif args.subcommand_c == 's':	
			create_output(args.path,args.name,args.div_word,args.trim)
		
if __name__ == '__main__':
	main()
