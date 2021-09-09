import pandas as pd
import igraph as gr

dataframe = pd.read_csv('wikispeedia_paths-and-graph/paths_finished.tsv',header = None, sep = '\t', comment = '#')
pathList = []
values = []
path=dataframe[3].dropna(how='any',axis=0)
for i in range(path.size):
    values += path[i].split(';')
    pathList += [(path[i].split(';'))]

x = 50
print(len(values))

values = list(set(values))
print(values)
#g = gr.Graph([('Banana','Apple'),('eggs','Banana')], directed = True)
#g.TupleList(edges=pathList[x], directed=True)
#g.TupleList([('Banana','Apple'),('eggs','Banana')], directed = True)
gr.plot(g, vertex_label = values)