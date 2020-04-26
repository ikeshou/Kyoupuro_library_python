from graphviz import Digraph, Graph


def make_graph_bellman():
    g = Digraph(format='png', comment='direct graph that contains negative weight path')
    g.attr('node', shape='circle')

    n = 10
    for i in range(n):
        g.node(str(i), label=str(i))

    edges = ((0, 1),
             (2, 0),
             (2, 3),
             (1, 4),
             (4, 5),
             (5, 2),
             (3, 6),
             (4, 7),
             (5, 8),
             (8, 9))

    edge_labels = [5, 6, 2, -2, -3, 4, 1, 7, 1, -1, -1]

    for i, e in enumerate(edges):
        g.edge(str(e[0]), str(e[1]), label=str(edge_labels[i]))

    g.render('graph_bellman', view=True, cleanup=True)



def make_graph_dijkstra():
    g = Graph(format='png', comment='undirected graph that contains no negative weight path')
    g.attr('node', shape='circle')

    n = 10
    for i in range(n):
        g.node(str(i), label=str(i))

    edges = ((0, 1),
             (2, 0),
             (2, 3),
             (1, 4),
             (4, 5),
             (5, 2),
             (3, 6),
             (4, 7),
             (5, 8),
             (8, 9))

    edge_labels = [5, 6, 2, 2, 3, 4, 1, 7, 1, 1, 1]

    for i, e in enumerate(edges):
        g.edge(str(e[0]), str(e[1]), label=str(edge_labels[i]))

    g.render('graph_dijkstra', view=True, cleanup=True)    



def make_graph_mst():
    g = Graph(format='png', comment='undirected graph that contains no negative weight path')
    g.attr('node', shape='circle')

    n = 9
    for i in range(n):
        g.node(str(i), label=str(i))

    edges = ((0, 1),
             (0, 7),
             (1, 2),
             (1, 7),
             (2, 3),
             (2, 5),
             (2, 8),
             (3, 4),
             (3, 5),
             (4, 5),
             (5, 6),
             (6, 7),
             (6, 8),
             (7, 8))

    edge_labels = [4, 8, 8, 11, 7, 4, 2, 9, 14, 10, 2, 1, 6, 7]

    for i, e in enumerate(edges):
        g.edge(str(e[0]), str(e[1]), label=str(edge_labels[i]))

    g.render('graph_mst', view=True, cleanup=True)



def make_graph_flow():
    g = Digraph(format='png', comment='direct graph that does not contain negative weight path')
    g.attr('node', shape='circle')

    n = 10
    for i in range(n):
        g.node(str(i), label=str(i))

    edges = ((0, 1), (0, 2), (0, 3),
             (1, 2), (1, 4),
             (2, 6),
             (3, 2), (3, 7),
             (4, 5), (4, 9),
             (5, 1), (5, 2), (5, 6), (5, 9),
             (6, 8),
             (7, 6),
             (8, 7), (8, 9))

    edge_labels = [50, 20, 30, 10, 10, 40, 10, 20, 10, 20, 30, 20, 10, 10, 50, 10, 20, 50]

    for i, e in enumerate(edges):
        g.edge(str(e[0]), str(e[1]), label=str(edge_labels[i]))

    g.render('graph_flow', view=True, cleanup=True)


def make_bipartite_graph():
    g = Graph(format='png', comment='undirected graph that contains no negative weight path', engine='dot')
    g.attr('node', shape='circle')

    n = 10
    with g.subgraph(name='cluster_0') as c:
        c.attr(label='process #1')
        for i in range(0, n, 2):
            c.node(str(i), label=str(i), color='blue')

    with g.subgraph(name='cluster_1') as c:
        c.attr(label='process #2')
        for i in range(1, n, 2):
            c.node(str(i), label=str(i), color='red')
    
    edges = ((0, 1),
             (1, 2), (1, 4),
             (2, 9),
             (3, 4),
             (4, 5), (4, 9),
             (5, 6),
             (6, 7), (6, 9),
             (8, 9))
    
    for e in edges:
        g.edge(str(e[0]), str(e[1]))

    g.render('graph_bipartite', view=True, cleanup=True)



if __name__ == "__main__":
    # make_graph_bellman()
    # make_graph_dijkstra()
    # make_graph_mst()
    # make_graph_flow()
    make_bipartite_graph()
         
