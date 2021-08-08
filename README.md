Instructions for running the program:

Directory structure:
	-The directory data_raw contains .fasta- and .len-files. The fasta must
	 be an alignment and contains data that is not split. The len-file must 
	 contain the positions to split the data.
	 
	-The directory phylogenetical trees contains newick-files of the
	 topologicaly correct trees.
	
	-The directory preprocessed_data contains fasta-files which are ready to
	 be processed by the program.
	 
	-The directory results contains the results after executing the program.
	
	-The directory compare contains several graphical outputs produced by
	 the plot script.
	 
Usage:
	To start the program, the script '__main__.py' must be started in the 
	directory 'Source Code' via: python3 __main__.py
	The program works on command-line-arguments. Arguments starting with '-'
	are optional, all other options are positional. Numbers 2,3,4 and 5 are 
	mutually exclusive.
	It accepts the following arguments:
	
	1. -h,-help: Displays required and optional arguments. This can also be
		     be called on every level.
	2. nt: Compare two newick-trees
		2.1 path1: Name of the first newick-file lying in directory 
			   'results'
		2.2 path2: Name of the second newick-file lying in directory
			   'phylogenetical trees'
	3. s: Split a fasta file stored in the directory 'data_raw'
		3.1 name: Name of the fasta-file
	4. cr: Create a fasta-file filled with randomized strings
		4.1 letters: Alphabet of which the strings are generated
		4.2 n: Number of strings constructed
		4.3 m: Length of constructed strings
	5. com: Run the main program.
		5.1 -trim: Trim the input file(s) to contain only the letters
			   'ACGT'
		5.2 -div_word: Compute a lexicographically smallest minimal
				diverging word
		5.3 -lev: Compute the Levenshtein-Distance alongside 
			  MAXSIMK-Distance
		5.4 -lcs: Compute the LCS-Distance alongside MAXSIMK-Distance
		5.5 -correct: Check the implementation of MAXSIMK via 
			      Simon-Trees for correctness by comparing with an
			      implementation based on shortlex-normalforms.
		5.6 s: Process a single fasta-file
			5.6.1: name: Name of the fasta-file
		5.7 a: Process all fasta-files in the directory 
			'preprocessed_data'
