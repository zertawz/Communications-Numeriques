# Code of the first try:
import numpy as np
import dahuffman
import matplotlib.pyplot as plt
import math

#Open the file
f = open("The_Adventures_of_Sherlock_Holmes_A_Scandal_In_Bohemia.txt")
message = f.read()
f.close

dic={}
for i in message:
    if i not in dic.keys(): 
        dic[i] = 1/len(message)
    else:
        dic[i] += 1/len(message)

# histogramme
caracteres = list(dic.keys())
probas = list(dic.values())
"""
plt.bar(caracteres, probas)
"""

# Calcul de l'entropie
entropie = math.log(len(caracteres),2)

# Codage huffman
codec = dahuffman.HuffmanCodec.from_data(message)
#codec.print_code_table()
table_codage = dahuffman.get_code_table()
print(table_codage)
