"""
Solves for optimal EO solution. Note that this representation is quite
minimal, in that only edges will be considered, and only their orientation. An edge is
considered oriented if it can reach its correct location using only <F2, B2, U, D, R, L>.

Nodes are represented as binary lists; where 0 represents a correctly oriented edge, and 1
an incorrectly oriented one. The indices correspond to edges ordered clockwise (starting from the top
, or top-right corner of the face), as seen from the front; in layers from the front to the back:


               ................8................/\
              /          /          /          /  \
             /          /          /          /    \
            /          /          /          /      \
           /----------/----------/----------/\      /\
          /          /          /          /  \    /  \
         7          /          /          4    \  /    9
        /          /          /          /      \/      \
       /----------/----------/----------/\      /\      /\
      /          /          /          /  \    /  \    /  \
     /          /          /          /    \  /    \  /    \
    /          /          /          /      \/      \/      \
    \----------\----0-----\----------\      /\      /\      /
     \          \          \          \    /  \    /  \    /
      \          \          \          \  /    \  /    \  /
       \          \          \          \/      \/      \/
        \----------\----------\----------\      /\      /
         \          \          \          \    /  \    5
          3          \          \          1  /    \  /
           \          \          \          \/      \/
            \----------\----------\----------\      /
             \          \          \          \    /
              \          \          \          \  /
               \..........\....2.....\..........\/

AS SEEN FROM ABOVE:

       UP:                  EQUATOR:                DOWN:
________________       ________________       ________________
|    |    |    |       |    |    |    |       |    |    |    |
|    | 8  |    |       | 11 |    | 9  |       |    | 10 |    |
|____|____|____|       |____|____|____|       |____|____|____|
|    |    |    |       |    |    |    |       |    |    |    |
| 7  |    | 4  |       |    |    |    |       | 6  |    | 5  |
|____|____|____|       |____|____|____|       |____|____|____|
|    |    |    |       |    |    |    |       |    |    |    |
|    | 0  |    |       | 3  |    | 1  |       |    | 2  |    |
|____|____|____|       |____|____|____|       |____|____|____|

"""
import networkx as nx
import pickle



def toList(s):
    """
    Converts string representing orientation to list of ints
    """
    return [int(s[i]) for i in range(len(s))]

def toString(l):
    """
    Converts list representation to string
    """
    output = ""
    for c in l: output += str(c)
    return output

with open('eo.graph', 'rb') as filename:
    G = pickle.load(filename)

paths = nx.algorithms.shortest_paths.generic.shortest_path(G, "0"*12)

# path = paths["111111111111"]
# print(path)
# for i in range(len(path) - 1):
#     print(G.edges[path[i], path[i+1]]['label'])


maxlength = 0
farthest = []
algs = []
for target in paths:
    path = paths[target].copy()
    if len(path) > maxlength:
        farthest = []
        algs = []
        maxlength = len(path)
    if len(paths[target]) >= maxlength:
        farthest.append(target)
        alg = ""
        for i in range(len(path) - 1):
            alg += G.edges[path[i], path[i+1]]['label']
        algs.append(alg)
print(maxlength)
print(farthest)
print(algs)
