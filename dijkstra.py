import numpy
import time
from graph import Graph
import GraphGenerator
from data_structure.minheap import MinHeap as MinHeap
from data_structure.DanielBorowskiFibonacciHeap import FibonacciHeap as DBFibonacciHeap
from data_structure.FibHeap import Fheap as FibHeap
from data_structure.KeithSchwarzFibonacciHeap import KFib as KFib

DATA_FOLDER_NAME = "data7"


def format_time(time_in_seconds):
    return int(time_in_seconds*1000)


def dijkstra_with_fibonacci_heap(graph, queue):
    temp_dist = numpy.empty(graph.node_number, dtype=object)
    temp_dist.fill(numpy.inf)
    temp_dist[graph.source_node] = 0;
    final_distances = temp_dist.copy()
    node_array = [None] * graph.node_number

    complete = numpy.empty(graph.node_number, dtype=object)
    complete.fill(False)

    init_heap = getattr(queue, "init_heap", None)
    if callable(init_heap):
        queue.init_heap(graph.node_number)
    node_array[graph.source_node] = queue.insert(temp_dist[graph.source_node], graph.source_node)
    for index in range(graph.node_number):
        minimum = queue.extract_min()
        if minimum is None:
            break
        for edge in graph.edges[minimum.value]:
            if not complete[edge[0]]:
                if node_array[edge[0]] is not None:
                    if node_array[edge[0]].key > edge[1] + minimum.key:
                        queue.decrease_key(node_array[edge[0]], edge[1] + minimum.key)
                else:
                    node_array[edge[0]] = queue.insert(edge[1] + minimum.key, edge[0])
        complete[minimum.value] = True
        final_distances[minimum.value] = minimum.key
    return final_distances


def dijkstra_with_fibonacci_heap_no_decrease_key(graph, queue):
    temp_dist = numpy.empty(graph.node_number, dtype=object)
    temp_dist.fill(numpy.inf)
    temp_dist[graph.source_node] = 0;
    final_distances = temp_dist.copy()
    node_array = [None] * graph.node_number

    complete = numpy.empty(graph.node_number, dtype=object)
    complete.fill(False)

    init_heap = getattr(queue, "init_heap", None)
    if callable(init_heap):
        queue.init_heap(graph.node_number)

    node_array[graph.source_node] = queue.insert(temp_dist[graph.source_node], graph.source_node)
    for index in range(graph.node_number):
        minimum = queue.extract_min()
        if minimum is None:
            break
        for edge in graph.edges[minimum.value]:
            if not complete[edge[0]] and (not (not (node_array[edge[0]] is None) and not (
                    node_array[edge[0]] is not None and node_array[edge[0]].key > edge[1] + minimum.key))):
                node_array[edge[0]] = queue.insert(edge[1] + minimum.key, edge[0])
        complete[minimum.value] = True
        final_distances[minimum.value] = minimum.key
    return final_distances


def run_algorithm(graph, queue, alg_name, output_file_name, test_times_file, fib_times_file_path, has_decrease_key):
    fib_times_file = open(fib_times_file_path, "a")
    times = []
    for iterator in range(1, 11):
        start_time = time.time()
        # taking advantage of the fact that at the end of the algorithm, the queue is empty,
        # there is no need to pass a new queue every time
        if has_decrease_key:
            distances = dijkstra_with_fibonacci_heap(graph, queue)
        else:
            distances = dijkstra_with_fibonacci_heap_no_decrease_key(graph, queue)
        end_time = time.time()
        print("Run time for run {} {} solution:{} milliseconds".format(iterator, alg_name, format_time(end_time - start_time)))
        test_times_file.write(
            "Run time for run {} {} solution:{} milliseconds\n".format(iterator, alg_name, format_time(end_time - start_time)))
        times.append(format_time(end_time - start_time))
    f = open(output_file_name, "w")
    for distance in distances:
        f.write("{} ".format(distance))
    f.close()

    times.sort()
    final_times = [times[t] for t in range(2, 8)]
    average_time = int(sum(final_times) / len(final_times))
    print("Average time for {} solution is {}".format(alg_name, average_time))
    test_times_file.write("Average time for {} solution is {}\n".format(alg_name, average_time))
    fib_times_file.write("{}\n".format(average_time))
    fib_times_file.close()


def run_algorithms(graph, test_number):
    times_file = open("{}/testTimes.txt".format(DATA_FOLDER_NAME), "a")
    print("Running test on graph with {} nodes and {} edges".format(graph.node_number, graph.edge_number))
    times_file.write(
        "\nRunning test on graph with {} nodes and {} edges\n".format(graph.node_number, graph.edge_number))

    #run_dijkstra_with_min_heap(graph, "min heap", "{}/heap{}.txt".format(DATA_FOLDER_NAME, test_number), times_file, "{}/heapTimes.txt".format(DATA_FOLDER_NAME), True)
    run_algorithm(graph, MinHeap(), "min heap", "{}/heap{}.txt".format(DATA_FOLDER_NAME, test_number), times_file, "{}/heapTimes.txt".format(DATA_FOLDER_NAME), True)

    # Fibonacci heap implementations
    run_algorithm(graph, DBFibonacciHeap(), "fib heap", "{}/fibdb{}.txt".format(DATA_FOLDER_NAME, test_number), times_file, "{}/fibdb.txt".format(DATA_FOLDER_NAME), True)
    run_algorithm(graph, FibHeap(), "fibPip heap", "{}/fibPip{}.txt".format(DATA_FOLDER_NAME, test_number), times_file, "{}/fibPip.txt".format(DATA_FOLDER_NAME), True)
    run_algorithm(graph, KFib(), "fibK heap", "{}/fibK{}.txt".format(DATA_FOLDER_NAME, test_number), times_file, "{}/fibK.txt".format(DATA_FOLDER_NAME), True)

    #run_dijkstra_with_min_heap(graph, "min heapi", "{}/heapi{}.txt".format(DATA_FOLDER_NAME, test_number), times_file, "{}/heapTimes.txt".format(DATA_FOLDER_NAME), False)


    #No decrease key tests
    run_algorithm(graph, MinHeap(), "min heap2", "{}/heap{}2.txt".format(DATA_FOLDER_NAME, test_number), times_file, "{}/heapTimes2.txt".format(DATA_FOLDER_NAME), False)

    # Fibonacci heap implementations
    run_algorithm(graph, DBFibonacciHeap(), "fib heapi", "{}/fibdbi{}.txt".format(DATA_FOLDER_NAME, test_number), times_file, "{}/fibdbi.txt".format(DATA_FOLDER_NAME), False)
    run_algorithm(graph, FibHeap(), "fibPip heapi", "{}/fibPipi{}.txt".format(DATA_FOLDER_NAME, test_number), times_file, "{}/fibPipi.txt".format(DATA_FOLDER_NAME), False)
    run_algorithm(graph, KFib(), "fibK heapi", "{}/fibKi{}.txt".format(DATA_FOLDER_NAME, test_number), times_file, "{}/fibKi.txt".format(DATA_FOLDER_NAME), False)

    times_file.close()
    print("Done")


def main():
    edges = [5000, 10000, 50000, 100000, 200000, 300000, 400000, 500000, 600000, 700000]
    nodes = 1000
    max_weight = 1000000
    source = 0
    for test_no in range(len(edges)):
        for graph_no in range(20):
            file_id = "{}{}".format(test_no, graph_no)
            print("Running test number {}, iteration {}".format(test_no, graph_no))
            if graph_no < 10:
                GraphGenerator.generate_graph("{}/graph{}.txt".format(DATA_FOLDER_NAME, file_id), nodes, edges[test_no], source, max_weight)
            else:
                GraphGenerator.generate_graph_probability("{}/graph{}.txt".format(DATA_FOLDER_NAME, file_id), nodes, edges[test_no]/(nodes*nodes), source, max_weight)

            graph = Graph()
            graph.read_from_file("{}/graph{}.txt".format(DATA_FOLDER_NAME, file_id), True)

            run_algorithms(graph, file_id)


if __name__ == "__main__":
    main()
