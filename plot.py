import matplotlib.pyplot as plt
import os
import numpy as np
import distMat

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
plt.plot(x,z,label='LCS')
plt.legend()
plt.tick_params(
	axis='x',
	which='both',
	bottom=False,
	top=False,
	labelbottom=False
)
plt.savefig('distance_compare_lcs.png')

dm = distMat.normalize_dist_mat(distMat.get_dist_mat_from_file('/home/jakob/Dokumente/Bachelorarbeit/results/fish_mito/fish_mito.txt'))
plt.matshow(dm,cmap='Reds')
plt.colorbar()
plt.savefig('fish_mito.png')
plt.clf()


dm = distMat.normalize_dist_mat(distMat.get_dist_mat_from_file('/home/jakob/Dokumente/Bachelorarbeit/results/VgI10539-M2018-NT.ali.fa.ali/VgI10539-M2018-NT.ali.fa.ali.txt'))
plt.matshow(dm,cmap='Reds')
plt.colorbar()
plt.savefig('VgI10539-M2018-NT.ali.fa.ali.png')
