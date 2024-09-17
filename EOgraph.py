"""
Produce the graph of adjacencies for EO. Note that this representation is quite
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

def cycle(orientation, indices):
    """
    Given the current orientation (as a list), cycles the given indices in order.
    Assume the user knows what they're doing for now; add some checks later, e.g. nonempty lists
    and valid indices. (Also can be a bit sneakier here but I think it doesn't matter).
    """
    temp = orientation[indices[-1]]
    for i in range(len(indices) - 1):
        orientation[indices[-i-1]] = orientation[indices[-i-2]]
    orientation[indices[0]] = temp

def flip(orientation, indices):
    """
    Given the current orientation (as a list), flip the values of the given indices.
    Assume the user knows what they're doing for now; add some checks later, e.g. nonempty lists
    and valid indices.
    """
    for i in indices:
        orientation[i] = 1 - orientation[i]

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


vertices = [] # list of vertices, i.e. lists of orientations

for i in range(int(2 ** 11)):
    temp = ''
    count = 0
    for j in range(11):
        d = (i // int(2**j)) % 2
        temp += str(d)
        count += d
    temp += str(count % 2)
    vertices.append(temp)
# print(vertices)


turns = {
'U': [0,7,8,4],
'D': [2,5,10,6],
'R': [1,4,9,5],
'L': [3,6,11,7],
'F': [0,1,2,3],
'B': [8,11,10,9]
}

G = nx.DiGraph()

G.add_nodes_from(vertices)

for v in vertices:
    for t in turns:
        l = toList(v)
        cycle(l,turns[t])
        if(t == 'F' or t == 'B'):
            flip(l, turns[t])
        G.add_edge(v,toString(l),label = t)
        cycle(l,turns[t])
        if(t == 'F' or t == 'B'):
            flip(l, turns[t])
        G.add_edge(v,toString(l),label = t + "2")
        cycle(l,turns[t])
        if(t == 'F' or t == 'B'):
            flip(l, turns[t])
        G.add_edge(v,toString(l),label = t + "'")


with open('eo.graph', 'wb') as filename:
    pickle.dump(G, filename)
