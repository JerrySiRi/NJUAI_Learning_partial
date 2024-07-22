import pandas as pd
import numpy as np
df1=pd.read_csv("tiny_word_vectors.txt",sep=' ')
df = pd.read_table('tiny_word_vectors.txt', sep='\s+', header=None)
print(df)
print(df1)
