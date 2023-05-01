# Importing the libraries
from collections import defaultdict

'''
The below code is a python script for Computing MVF algorithm via Lemma 6.
The following steps are implemented in this python script:
    Input to be given: A description graph G = (V,E,L) and a vertex v ∈ V
    Expected Output: The MVF of v in G, i.e., mvf(G, v)
        1. V^* ← SCC(G)
        2. E^* ← condense(G, V^*)
        3. G^*   (V^*, E^*)
        4. for V^' ← V^* do
        5.	 wgt[V^']  ← null
        6. return maxWeight(G^*,scc(G,v), wgt)
        // Auxiliary Function
        7. Function maxWeight(G^*, V^',wgt):
        8.  current  ← 0
        9.  for W^' ∈ {U^'∈V^* | (V^',U^' )∈ E^*} do
        10.     if wgt[W^'] = null then
        11.         current  ← max(current, maxWeight(G^*, W^',wgt))
        12.     else
        13.         current  ← wgt[W^']
        14.     wgt[V^']   current + |V^' |
        15. return wgt[V^']

'''


# Tarjan's algorithm to find strongly connected components in a graph
def tarjan(graph):
    index = defaultdict(lambda: None)
    lowlink = defaultdict(lambda: None)
    stack = []
    on_stack = defaultdict(lambda: False)
    result = []

    # Defining a helper function to perform depth-first search and identify strongly connected components
    def strongconnect(node, i):
        index[node] = i
        lowlink[node] = i
        i += 1
        stack.append(node)
        on_stack[node] = True
        # Checking for each neighbor of the current node
        if node not in graph:
            graph[node] = []

        for neighbor in graph[node]:
            if index[neighbor] is None:
                i = strongconnect(neighbor, i)
                lowlink[node] = min(lowlink[node], lowlink[neighbor])
            elif on_stack[neighbor]:
                lowlink[node] = min(lowlink[node], index[neighbor])

        if lowlink[node] == index[node]:
            scc = []
            while True:
                neighbor = stack.pop()
                on_stack[neighbor] = False
                scc.append(neighbor)
                if neighbor == node:
                    break
            result.append(scc)

        return i

    i = 0
    # Performing the depth-first search for each node in the graph
    for node in list(graph):
        if index[node] is None:
            i = strongconnect(node, i)
    # Returning the list of strongly connected components
    return result


# Function to create the condensed graph from a graph and its strongly connected components
def condense(graph, sccs):
    condensed = {}
    graph_copy = graph.copy()  # create a copy of the graph dictionary
    for scc in sccs:
        scc_set = set(scc)
        for node in scc:
            neighbors = set(graph_copy[node]) if node in graph_copy else set()
            for neighbor in neighbors:
                if neighbor not in scc_set:
                    if tuple(scc) not in condensed:
                        condensed[tuple(scc)] = []
                    condensed[tuple(scc)].append(tuple(set(graph_copy[node])))
                    break
        if tuple(scc) not in condensed:
            condensed[tuple(scc)] = []
    return condensed


# Function to compute the maximum vertex weight in a graph
def max_weight(graph, vertex, weights):
    if weights[vertex] is not None:
        return weights[vertex]

    weight = 0
    for neighbor in graph[vertex]:
        neighbor_weight = max_weight(graph, neighbor, weights)
        weight = max(weight, neighbor_weight)

    weights[vertex] = weight + 1
    return weights[vertex]


# Function to compute the maximum vertex weight in a condensed graph
def maxWeight(condensed, v, weights):
    current = 0
    for scc in condensed:
        if (v, scc) in condensed:
            w_scc = tuple(condensed[(v, scc)])
            if weights[w_scc] is None:
                current = max(current, maxWeight(condensed, w_scc, weights))
            else:
                current = weights[w_scc]
            weights[scc] = current + len(scc)
    return weights[scc]


# Graph taken from example-product-0.ttl
G = {
    'ex:x1': ['ex:M', 'ex:F'],
    'ex:x2': ['ex:M']
}

# Find the strongly connected components in the graph
sccs = tarjan(G)

# Create the condensed graph from the original graph and its strongly connected components
condensed = condense(G, sccs)

# Compute the maximum vertex weight for each strongly connected component
v = 'ex:x2'
weights = {}
for scc in sccs:
    if v in scc:
        weights[tuple(scc)] = 1
    else:
        weights[tuple(scc)] = None

maxWeight(condensed, tuple(sccs[sccs.index([v])]), weights)

# Print the result
print("MVF of v in G:", max(filter(lambda x: x is not None, weights.values())))

