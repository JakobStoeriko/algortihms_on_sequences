import matplotlib.pyplot as plt
import os
import numpy as np

os.chdir('../compare')
x,y = np.loadtxt('word_length.txt',delimiter=';',unpack=True)
plt.xlabel('Wortlänge')
plt.ylabel('MAXSIMK durchschnittlich')
#plt.title('Zusammenhang von Wortlänge und MAXSIMK bei fester Alphabetgröße')
plt.plot(x,y)
plt.savefig('wordlength.png')
plt.clf()

x,y=np.loadtxt('alphabet_length.txt', delimiter=';',unpack=True)
plt.xlabel('Alphabetgröße')
plt.ylabel('MAXSIMK durchschnittlich')
#plt.title('Zusammenhang von Alphabetgröße und MAXSIMK bei fester Wortlänge')
plt.plot(x,y)
plt.savefig('alphabetsize.png')
plt.clf()

x,y,z = np.loadtxt('../results/r,s=4,c=50,l=1000/distance_compare_lev.txt',delimiter=',',unpack=True)
plt.plot(x,y,label='MAXSIMK-Distanz')
plt.plot(x,z,label='Levenshtein-Distanz')
plt.legend()
plt.tick_params(
	axis='x',
	which='both',
	bottom=False,
	top=False,
	labelbottom=False
)
plt.savefig('distance_compare_lev.png')
plt.clf()

x,y,z = np.loadtxt('../results/r,s=4,c=50,l=1000/distance_compare_lcs.txt',delimiter=',',unpack=True)
plt.plot(x,y,label='MAXSIMK-Distanz')
plt.plot(x,z,label='LCS-Distanz')
plt.legend()
plt.tick_params(
	axis='x',
	which='both',
	bottom=False,
	top=False,
	labelbottom=False
)
plt.savefig('distance_compare_lcs.png')

dm = np.loadtxt('/home/jakob/Dokumente/Bachelorarbeit/results/fish_mito/distance_matrix.txt',delimiter=',')
plt.matshow(dm,cmap='Reds')
plt.colorbar()
plt.savefig('fish_mito.png')
plt.clf()


dm = np.loadtxt('/home/jakob/Dokumente/Bachelorarbeit/results/VgI10539-M2018-NT.ali.fa.ali/distance_matrix.txt',delimiter=',')
plt.matshow(dm,cmap='Reds')
plt.colorbar()
plt.savefig('VgI10539-M2018-NT.ali.fa.ali.png')
