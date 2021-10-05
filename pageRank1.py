import pandas as pd
import igraph as gr
import numpy as np
import time 

Beta_parameter = 0.85
epsilon = 0.001

def fixDepart(l):
    try:
        i_to_delete = l.index('<')
    except ValueError:
        return
    while '<' in l:
        count = 1 
        while (i_to_delete < len(l)-1 and l[i_to_delete + 1] == '<'):
            count += 1
            i_to_delete =  i_to_delete + 1
        l[i_to_delete] = l[i_to_delete - 2*count] 
        for i in range(1,count):
            l.pop(i_to_delete-i)  
        l.pop(i_to_delete-count)
        try:
            i_to_delete = l.index('<', i_to_delete-count)
        except ValueError:
            break


def fixEnd(l):
    try:
        i_to_delete = l.index('<')
    except ValueError:
        return
    while '<' in l:
        l.pop(i_to_delete)
        try:
            i_to_delete = l.index('<', i_to_delete)
        except ValueError:
            break

dataframe = pd.read_csv('wikispeedia_paths-and-graph/paths_finished.tsv',header = None, sep = '\t', comment = '#')

start = []
end = []
paths=dataframe[3]
for path in paths:
    path_string = path.split(';')
    a = path_string[:-1]
    fixDepart(a)
    b = path_string[1:]
    fixEnd(b)
    start += a
    end += b

graph_df = pd.DataFrame()
graph_df['start'] = start
graph_df['end'] = end


g = gr.Graph.DataFrame(graph_df)
#gr.plot(g, vertex_size = 10, edge_arrow_size = 0.4, edge_width = 0.5)
gr.summary(g)
# PageRank avec iGraph
# print(g.pagerank())

A = np.array(g.get_adjacency().data).T
sums = A.sum(axis=0, keepdims = 0)
sums[sums == 0] = 1

A_norm = A/sums
N = A_norm.shape[1]

# Une deuxième méthode de calcul de la matrice de transition, en utilisant la chaine de markov
"""
#Fonction qui retourne un dictionnaire pour chaque source donnée avec chaine de markov (target[key], probability[value])
def weight_source(g,vertex):
    l = []
    source = vertex.attributes()['name']
    for e in vertex.incident(mode='out'):
        l += [g.vs[e.target].attributes()['name']]
    data = {x:l.count(x)/len(l) for x in l}
    return source, data

df_index =[]
data =[]
# Boucle sur chaque vertex
for vertex in g.vs:
    i, buff = weight_source(g,vertex)
    df_index.append(i)
    data.append(buff)

#df_index contient le nom des vertex, data contient la ligne (target) pour chaque index
mx_markov = pd.DataFrame(data, index=df_index, columns=df_index)    # index = columns pour avoir une matrice NxN
mx_markov.fillna(0, inplace = True) #Remplacer les NaN
#print(mx_markov) 

# Stochastic matrix (P.T)
#A_norm= mx_markov.to_numpy().T
"""

# Calcul vecteur propre
# A est une matrice numpy, r_vector est notre vecteur d'essai, Beta est le damping factor, k est notre nombre de noeud (k!=N si PageRank persionnalisé)
def powermethod(A,r_vector,Beta_parameter,k):
    P_q = A.dot(r_vector)
    r_vector = Beta_parameter*P_q + (1-Beta_parameter)*(np.sum(r_vector))/k
    return r_vector




# Initialisation du vecteur
b_k_1 = np.full(N,1)

# Méthode de la puissance - execution
start_time = time.time()
b_k = powermethod(A_norm,b_k_1,Beta_parameter,N)

iter = 1
while ((b_k_1 - b_k) > epsilon).any() :
    b_k_1 = b_k
    b_k = powermethod(A_norm,b_k_1,Beta_parameter,N)
    iter += 1

# Temps d'execution de l'algorithme et nombre d'itération
print(time.time() - start_time, iter)

# Liste finale du PageRank, avec le nom des pages en index
ranking_df = pd.DataFrame(b_k,index=g.vs()["name"], columns=['rank'])

print(ranking_df.sort_values(by=['rank'], ascending=False).head(n=20))



# PageRank Personnalisé
# Mehdi Moussaif : M.M ==> un seul noeud : ligne 26
print(ranking_df.index[13])
# Initialisation du vecteur
b_k_1 = np.full(N,0)
b_k_1[13] = 1

# Méthode de la puissance avec 1 noeud - execution
b_k = powermethod(A_norm,b_k_1,Beta_parameter,1)

while ((b_k_1 - b_k) > epsilon).any() :
    b_k_1 = b_k
    b_k = powermethod(A_norm,b_k_1,Beta_parameter,1)
    iter += 1
ranking_df['rank'] = b_k
print(ranking_df.sort_values(by=['rank'], ascending=False).head(n=20))