Das Skript erlaubt die Verarbeitung von fasta-files.
Es hat 4 Modi:
1.  Aufruf: python3 __main__.py r Alphabet number length - Erzeugt ein fasta-file mit zufällig generierten Strings der angegebenen Anzahl und Länge.
2. Aufruf: python3 __main__.py s name - Erlaubt das splitten von Genen in einem fasta-file. Das Skript nimmt an, dass sich das fasta-file sowie das dazugehörige table-file in einem Ordner mit dem angegebenen Namen im Ordner data_raw, welcher sich eine Ebene höher als das Skript befindet, liegen.
3. Aufruf: python3 __main__.py c s name - Verarbeitet fasta-files im Ordner mit angegebenem Namen, welcher sich im Ordner preprocessed_data befindet. Der Ordner preprocessed_data muss auf einer Ebene höher als das Skript befinden.
Generiert den zugehörigen Newick Tree sowie eine Datei mit einer Übersicht über die paarweise berechneten Werte für max_sim_k
4. Aufruf: python3 __main__.py c a - Verarbeitet alle fasta-files die sich in Ordnern in preprocessed_data befinden so wie unter 3. angegeben.
