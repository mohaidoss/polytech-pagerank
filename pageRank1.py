import pandas as pd
import igraph as gr

dataframe = pd.read_csv('wikispeedia_paths-and-graph/paths_finished.tsv',header = None, sep = '\t', comment = '#')
print(dataframe[3][0])
list = []
path=dataframe[3].dropna(how='any',axis=0)
for i in range(path.size):
    list += [(path[i].split(';'))]
print(list[1])
g = gr.Graph()
g.TupleList(edges=list, directed=True)
gr.plot(g)