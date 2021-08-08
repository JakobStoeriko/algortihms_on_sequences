import matplotlib.pyplot as plt
import os
import numpy as np

fstring = 'Reds'
cmap = plt.cm.get_cmap(fstring).copy()
cmap.set_bad(color='blue')

os.chdir('../compare')
### plot wordlength
x,y = np.loadtxt('word_length.txt',delimiter=';',unpack=True)
plt.xlabel('Wortlänge')
plt.ylabel('MAXSIMK durchschnittlich')
plt.plot(x,y)
plt.savefig('wordlength.png')
plt.clf()


#plot alphabetsize
x,y=np.loadtxt('alphabet_length.txt', delimiter=';',unpack=True)
plt.xlabel('Alphabetgröße')
plt.ylabel('MAXSIMK durchschnittlich')
plt.plot(x,y)
plt.savefig('alphabetsize.png')
plt.clf()


#plot levenshtein distance matrix
dm = np.loadtxt('../results/r,s=4,c=50,l=1000/lev_dist_mat.txt',delimiter=',')
np.fill_diagonal(dm, np.nan)
plt.matshow(dm,cmap=cmap)
plt.xlabel('Wortnummer')
cbar = plt.colorbar()
cbar.ax.set_ylabel('Levenshtein-Distanz', rotation=270, labelpad=10)
plt.savefig('lev_dist_mat.png')
plt.clf()

#plot lcs distance matrix
dm = np.loadtxt('../results/r,s=4,c=50,l=1000/lcs_dist_mat.txt',delimiter=',')
np.fill_diagonal(dm, np.nan)
plt.matshow(dm,cmap=cmap)
plt.xlabel('Wortnummer')
cbar = plt.colorbar()
cbar.ax.set_ylabel('LCS-Distanz', rotation=270, labelpad=10)
plt.savefig('lcs_dist_mat.png')
plt.clf()

#plot maxsimk distance matrix
dm = np.loadtxt('../results/r,s=4,c=50,l=1000/distance_matrix.txt',delimiter=',')
np.fill_diagonal(dm, np.nan)
plt.matshow(dm,cmap=cmap)
plt.xlabel('Wortnummer')
cbar = plt.colorbar()
cbar.ax.set_ylabel('MAXSIMK-Distanz', rotation=270, labelpad=10)
plt.savefig('dist_mat.png')
plt.clf()

#plot maxsimk distance matrix for fish mito
dm = np.loadtxt('/home/jakob/Dokumente/Bachelorarbeit/results/fish_mito/distance_matrix.txt',delimiter=',')
np.fill_diagonal(dm, np.nan)
plt.matshow(dm,cmap=cmap)
plt.xlabel('Wortnummer')
cbar = plt.colorbar()
cbar.ax.set_ylabel('MAXSIMK-Distanz', rotation=270, labelpad=10)
plt.savefig('fish_mito.png')
plt.clf()

#plot maxsimk distance matrix for VgI
dm = np.loadtxt('/home/jakob/Dokumente/Bachelorarbeit/results/VgI10539-M2018-NT.ali.fa.ali/distance_matrix.txt',delimiter=',')
np.fill_diagonal(dm, np.nan)
plt.matshow(dm,cmap=cmap)
plt.xlabel('Wortnummer')
cbar = plt.colorbar()
cbar.ax.set_ylabel('MAXSIMK-Distanz', rotation=270, labelpad=10)
plt.savefig('VgI10539-M2018-NT.ali.fa.ali.png')
