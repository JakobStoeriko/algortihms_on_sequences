import matplotlib.pyplot as plt
import os
import numpy as np

os.chdir('../compare')
x,y = np.loadtxt('word_length.txt',delimiter=';',unpack=True)
plt.xlabel('Wortlänge')
plt.ylabel('MAXSIMK durchschnittlich')
plt.title('Zusammenhang von Wortlänge und MAXSIMK bei fester Alphabetgröße')
plt.plot(x,y)
plt.savefig('wordlength.png')
plt.clf()

x,y=np.loadtxt('alphabet_length.txt', delimiter=';',unpack=True)
plt.xlabel('Alphabetgröße')
plt.ylabel('MAXSIMK durchschnittlich')
plt.title('Zusammenhang von Alphabetgröße und MAXSIMK bei fester Wortlänge')
plt.plot(x,y)
plt.savefig('alphabetsize.png')
