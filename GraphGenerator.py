import random


def generate_graph(file_name, nodes, edges, start, max_weight):
    f = open(file_name, "a")
    f.write("{} {} {}\n".format(nodes, edges, start))
    edges_remaining = edges
    for node in range(nodes):
        number_of_edges = (random.sample(range(int(edges_remaining/(nodes-node) * 0.8), int(edges_remaining/(nodes-node) * 1.2)+1), 1))[0]
        if number_of_edges > edges_remaining or node == nodes-1:
            number_of_edges = edges_remaining

        edge_list = random.sample([i for i in range(nodes) if i not in [node]], number_of_edges)
        for edge in edge_list:
            f.write("{} {} {}\n".format(node, edge, (random.sample(range(1, max_weight + 1), 1))[0]))
        edges_remaining -= number_of_edges


def generate_graph_probability(file_name, nodes, probability, start, max_weight):
    max_value = int(probability*1000)
    edges = 0
    graph = [[] for i in range(nodes)]
    for source in range(nodes):
        for target in range(nodes):
            if random.randrange(1000) < max_value:
                edges += 1
                graph[source].append([target, random.randrange(1, max_weight+1)])
        random.shuffle(graph[source])

    f = open(file_name, "a")
    f.write("{} {} {}\n".format(nodes, edges, start))
    for node in range(nodes):
        for edge in graph[node]:
            f.write("{} {} {}\n".format(node, edge[0],edge[1]))
