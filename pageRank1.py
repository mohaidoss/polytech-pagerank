import pandas as pd
import igraph as gr

def fixDepart(l):
    i_to_delete = l.index('<')
    while '<' in l:
        count = 1 
        while (i_to_delete < len(l) and l[i_to_delete + 1] == '<'):
            count += 1
            i_to_delete =  i_to_delete + 1
        l[i_to_delete] = l[i_to_delete - 2*count] 
        for i in range(1,count):
            l.pop(i_to_delete-i)  
        l.pop(i_to_delete-count)
        try:
            i_to_delete = l.index('<', i_to_delete+1)
        except ValueError:
            break


def fixEnd(l):
    i_to_delete = l.index('<')
    while '<' in l:
        l.pop(i_to_delete)
        try:
            i_to_delete = l.index('<', i_to_delete+1)
        except ValueError:
            break

dataframe = pd.read_csv('wikispeedia_paths-and-graph/paths_finished.tsv',header = None, sep = '\t', comment = '#')

start = []
end = []
paths=dataframe[3].dropna(how='any',axis=0)
for path in paths:
    start += path.split(';')[:-1]
    end += path.split(';')[1:]
print('fixing depart')
fixDepart(start)
print('fixing end')
fixEnd(end)
