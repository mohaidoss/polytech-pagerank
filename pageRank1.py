import pandas as pd
import igraph as gr

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

print(len(start),len(end))

x = ['a','b','c','d','e','<','<','<','z']
fixDepart(x)
print(x)