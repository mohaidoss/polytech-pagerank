import pandas as pd
import igraph as gr

dataframe = pd.read_csv('wikispeedia_paths-and-graph/paths_finished.tsv',header = None, sep = '\t', comment = '#')
print(dataframe[3][0])
list = []
for i in range(dataframe[3].size):
    list += [(dataframe[3][i].split(';'))]
    
gr.Graph.TupleList(edges=list)