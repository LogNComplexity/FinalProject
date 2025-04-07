import heapq
import math
from math import radians, cos, sin, asin, sqrt
import os
import random
import time
import timeit 
import matplotlib.pyplot as plt
import numpy as np
import math
import sys




def draw_plot(run_arr1, mean1, blueBars ,run_arr2, mean2, redBars, case):
    x1 = np.arange(0, len(run_arr1), 1)
    x2 = np.arange(len(run_arr1), len(run_arr1) + len(run_arr2), 1)

    fig = plt.figure(figsize=(20, 8))

    # Plot first array in blue
    plt.bar(x1, run_arr1, color="blue", label= blueBars)

    # Plot second array in red
    plt.bar(x2, run_arr2, color="red", label= redBars)

    # Mean lines
    plt.axhline(mean1, color="blue", linestyle="--", linewidth = 2 ,label="Avg"+ blueBars, xmin = 0.5, xmax= 1)
    plt.axhline(mean2, color="red", linestyle="--", linewidth = 2 ,label="Avg" + redBars, xmin = 0, xmax = 0.5)

    plt.xlabel("Iterations")
    plt.ylabel("Run time")
    plt.title("Run time for " + blueBars +" in blue and "+ redBars+" in red " + case)

    plt.legend()
    plt.show()



class UnDirectedWeightedGraph:

    def __init__(self):
        self.adj = {}
        self.weights = {}
        self.coordinates = {}

    def adjacent_nodes(self, node):
        return self.adj[node]
    
    def add_coordinate(self,node, lat, lon):
        self.coordinates[node] = (lat,lon)

    def add_node(self, node):
        if node not in self.adj:   # Only add if not already present
            self.adj[node] = []

    def add_edge(self, node1, node2, weight):
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
            self.adj[node2].append(node1)
        self.weights[(node1, node2)] = weight
        self.weights[(node2, node1)] = weight

    def get_weight(self, node1, node2):
        
        return self.weights[(node1, node2)]
    
    def get_coordinates(self):
        return self.coordinates
        

    def get_graph(self,):
        return self.adj



def create_random_undirected_weighted_graph(num_nodes, edge_probability=0.3, min_weight=1, max_weight=10):

    graph = UnDirectedWeightedGraph()

    for i in range(num_nodes):
        graph.add_node(i)

    # for each unique unordered pair of nodes, consider adding an edge
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < edge_probability:
                weight = random.randint(min_weight, max_weight)
                graph.add_edge(i, j, weight)
    
    # graph.get_graph()
    return graph






class Item:
    def __init__(self, value, key):
        self.key = key
        self.value = value
    
    def __str__(self):
        return "(" + str(self.key) + "," + str(self.value) + ")"

class Heap:
    def __init__(self, data):
        self.items = data
        self.length = len(data)
        
        # add a map based on input node
        self.map = {}
        for i in range(self.length):
            self.map[self.items[i].value] = i

        self.build_heap()

    def find_left_index(self,index):
        return 2 * (index + 1) - 1

    def find_right_index(self,index):
        return 2 * (index + 1)

    def find_parent_index(self,index):
        return (index + 1) // 2 - 1  
    
    def heapify(self, index):
        smallest_known_index = index

        if self.find_left_index(index) < self.length and self.items[self.find_left_index(index)].key < self.items[index].key:
            smallest_known_index = self.find_left_index(index)

        if self.find_right_index(index) < self.length and self.items[self.find_right_index(index)].key < self.items[smallest_known_index].key:
            smallest_known_index = self.find_right_index(index)

        if smallest_known_index != index:
            self.items[index], self.items[smallest_known_index] = self.items[smallest_known_index], self.items[index]
            
            # update map
            self.map[self.items[index].value] = index
            self.map[self.items[smallest_known_index].value] = smallest_known_index

            # recursive call
            self.heapify(smallest_known_index)

    def build_heap(self,):
        for i in range(self.length // 2 - 1, -1, -1):
            self.heapify(i) 

    def insert(self, node):
        if len(self.items) == self.length:
            self.items.append(node)
        else:
            self.items[self.length] = node
        self.map[node.value] = self.length
        self.length += 1
        self.swim_up(self.length - 1)

    def insert_nodes(self, node_list):
        for node in node_list:
            self.insert(node)

    def swim_up(self, index):
        
        while index > 0 and self.items[index].key < self.items[self.find_parent_index(index)].key:
            #swap values
            self.items[index], self.items[self.find_parent_index(index)] = self.items[self.find_parent_index(index)], self.items[index]
            #update map
            self.map[self.items[index].value] = index
            self.map[self.items[self.find_parent_index(index)].value] = self.find_parent_index(index)
            index = self.find_parent_index(index)

    def get_min(self):
        if len(self.items) > 0:
            return self.items[0]

    def extract_min(self,):
        #xchange
        self.items[0], self.items[self.length - 1] = self.items[self.length - 1], self.items[0]
        #update map
        self.map[self.items[self.length - 1].value] = self.length - 1
        self.map[self.items[0].value] = 0

        min_node = self.items[self.length - 1]
        self.length -= 1
        self.map.pop(min_node.value)
        self.heapify(0)
        return min_node

    def decrease_key(self, value, new_key):
        if new_key >= self.items[self.map[value]].key:
            return
        index = self.map[value]
        self.items[index].key = new_key
        self.swim_up(index)

    def get_element_from_value(self, value):
        return self.items[self.map[value]]

    def is_empty(self):
        return self.length == 0
    
    def __str__(self):
        height = math.ceil(math.log(self.length + 1, 2))
        whitespace = 2 ** height + height
        s = ""
        for i in range(height):
            for j in range(2 ** i - 1, min(2 ** (i + 1) - 1, self.length)):
                s += " " * whitespace
                s += str(self.items[j]) + " "
            s += "\n"
            whitespace = whitespace // 2
        return s








#############################################################################################################################
# PART 2
#############################################################################################################################

# 2.1
def dijkstra_k(graph, source, k):

    # initialize dictionaries using nodes in graph.adj
    dist = {node: float('inf') for node in graph.adj}
    path = {node: [] for node in graph.adj}
    relax_count = {node: 0 for node in graph.adj}

    # the source node's distance is 0 and its path is just [source]
    dist[source] = 0
    path[source] = [source]

    # initialize heap with all nodes, starting with source at 0
    node_objects = []
    for node in graph.adj:
        if node == source:
            node_objects.append(Item(node, 0))
        else:
            node_objects.append(Item(node, float('inf')))
    
    heap = Heap(node_objects)

    while not heap.is_empty():
        min_node = heap.extract_min()
        u = min_node.value
        current_distance = min_node.key

        for v in graph.adj[u]:
            weight = graph.get_weight(u, v)
            if relax_count[v] < k:
                new_distance = dist[u] + weight
                if new_distance < dist[v]:
                    dist[v] = new_distance
                    path[v] = path[u] + [v]
                    relax_count[v] += 1
                    heap.decrease_key(v, new_distance)

    return dist, path

# 2.2
def bellman_k(graph, source, k):
    
    # initialize distances, paths, and relaxation counts
    dist = {node: float('inf') for node in graph.adj}
    path = {node: [] for node in graph.adj}
    relax_count = {node: 0 for node in graph.adj}
    
    # initialize source
    dist[source] = 0
    path[source] = [source]
    
    # keep trying to relax edges while something changes
    changed = True
    while changed:
        changed = False
        for u in graph.adj:
            if dist[u] == float('inf'):
                continue
            for v in graph.adjacent_nodes(u):
                weight = graph.get_weight(u, v)
                # relax only if v has been relaxed fewer than k times
                if relax_count[v] < k and dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    path[v] = path[u] + [v]
                    relax_count[v] += 1
                    changed = True
                    
    # negative cycle detection: check if any edge can be relaxed further
    for u in graph.adj:
        if dist[u] == float('inf'):
            continue
        for v in graph.adjacent_nodes(u):
            weight = graph.get_weight(u, v)
            if dist[u] + weight < dist[v]:
                raise Exception("graph contains a negative cycle")
    
    return dist, path


# 2.3

###############################################
# helper functions

def measure_graph_space(graph):

    size = sys.getsizeof(graph.adj) + sys.getsizeof(graph.weights)
    for node, neighbors in graph.adj.items():
        size += sys.getsizeof(neighbors)
    return size

def measure_algo_space(dist, path, relax_count=None):

    size = sys.getsizeof(dist) + sys.getsizeof(path)
    if relax_count is not None:
        size += sys.getsizeof(relax_count)
    return size


def compute_accuracy(dist_true, dist_k):
    """
    compute the fraction of nodes for which the computed distance equals the ground truth

    """
    correct = 0
    total = len(dist_true)
    for node in dist_true:
        if dist_true[node] == float('inf') and dist_k[node] == float('inf'):
            correct += 1
        elif dist_true[node] == dist_k[node]:
            correct += 1
    return correct / total

#############################################################################################################################
# PART 2 experiment function
#############################################################################################################################

def experiment_2():

    graph_sizes = [50, 100, 200, 400]
    densities   = [0.1, 0.3, 0.5]
    k_values    = [3, 5, 10]  # k must be less than n-1
    num_trials  = 3

    results = {
        'graph_size': [],
        'density': [],
        'k': [],
        
        'dijkstra_time': [],
        'dijkstra_accuracy': [],
        'dijkstra_space': [],
        
        'bellman_ford_time': [],
        'bellman_ford_accuracy': [],
        'bellman_ford_space': []
    }
    
    for n in graph_sizes:
        for density in densities:
            for k in k_values:
                if k >= n - 1:
                    continue  # skip invalid k
                
                # lists to accumulate trial values
                d_times, d_accs, d_spaces = [], [], []
                b_times, b_accs, b_spaces = [], [], []
                
                for _ in range(num_trials):
                    # generate random graph
                    graph = create_random_undirected_weighted_graph(n, edge_probability=density, min_weight=1, max_weight=10)
                    
                    # measure space used by graph itself
                    base_space = measure_graph_space(graph)
                    
                    # get ground-truth distances (using full Dijkstra with k = n-1)
                    dist_true, _ = dijkstra_k(graph, 0, n-1)
                    
                    # -------------------------------
                    # A) k-relaxation Dijkstra
                    # -------------------------------
                    start = time.time()
                    dist_d, path_d = dijkstra_k(graph, 0, k)
                    d_elapsed = time.time() - start
                    
                    d_accuracy = compute_accuracy(dist_true, dist_d)
                    d_space = base_space + measure_algo_space(dist_d, path_d)
                    
                    d_times.append(d_elapsed)
                    d_accs.append(d_accuracy)
                    d_spaces.append(d_space)
                    
                    # -------------------------------
                    # B) k-relaxation Bellman-Ford
                    # -------------------------------
                    try:
                        start = time.time()
                        dist_b, path_b = bellman_k(graph, 0, k)
                        b_elapsed = time.time() - start
                        
                        b_accuracy = compute_accuracy(dist_true, dist_b)
                        b_space = base_space + measure_algo_space(dist_b, path_b)
                        
                        b_times.append(b_elapsed)
                        b_accs.append(b_accuracy)
                        b_spaces.append(b_space)
                    except Exception as e:
                        # in case of exception (negative cycle), record nothing for this trial
                        b_times.append(None)
                        b_accs.append(None)
                        b_spaces.append(None)
                
                # compute averages over the successful trials 
                valid_d_times  = [t for t in d_times if t is not None]
                valid_d_accs   = [a for a in d_accs if a is not None]
                valid_d_spaces = [s for s in d_spaces if s is not None]
                
                valid_b_times  = [t for t in b_times if t is not None]
                valid_b_accs   = [a for a in b_accs if a is not None]
                valid_b_spaces = [s for s in b_spaces if s is not None]
                
                avg_d_time  = sum(valid_d_times) / len(valid_d_times) if valid_d_times else None
                avg_d_acc   = sum(valid_d_accs) / len(valid_d_accs) if valid_d_accs else None
                avg_d_space = sum(valid_d_spaces) / len(valid_d_spaces) if valid_d_spaces else None
                
                avg_b_time  = sum(valid_b_times) / len(valid_b_times) if valid_b_times else None
                avg_b_acc   = sum(valid_b_accs) / len(valid_b_accs) if valid_b_accs else None
                avg_b_space = sum(valid_b_spaces) / len(valid_b_spaces) if valid_b_spaces else None
                
                results['graph_size'].append(n)
                results['density'].append(density)
                results['k'].append(k)
                
                results['dijkstra_time'].append(avg_d_time)
                results['dijkstra_accuracy'].append(avg_d_acc)
                results['dijkstra_space'].append(avg_d_space)
                
                results['bellman_ford_time'].append(avg_b_time)
                results['bellman_ford_accuracy'].append(avg_b_acc)
                results['bellman_ford_space'].append(avg_b_space)
    
    # -------------------------------
    # Plotting
    
    # --- Dijkstra Plots ---
    # 1) time
    plt.figure(figsize=(10, 5))
    for density in sorted(set(results['density'])):
        for k_ in sorted(set(results['k'])):
            xs = [results['graph_size'][i] for i in range(len(results['graph_size']))
                  if results['density'][i] == density and results['k'][i] == k_ and results['dijkstra_time'][i] is not None]
            ys = [results['dijkstra_time'][i] for i in range(len(results['graph_size']))
                  if results['density'][i] == density and results['k'][i] == k_ and results['dijkstra_time'][i] is not None]
            if xs:
                plt.plot(xs, ys, marker='o', label=f"Dijkstra: dens={density}, k={k_}")
    plt.xlabel("Graph Size (nodes)")
    plt.ylabel("Time (s)")
    plt.title("k-Relaxation Dijkstra: Time vs Graph Size")
    plt.ylim(bottom=0, top=max(ys)*1.1 if ys else 0.05)
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # 2) accuracy
    plt.figure(figsize=(10, 5))
    for density in sorted(set(results['density'])):
        for k_ in sorted(set(results['k'])):
            xs = [results['graph_size'][i] for i in range(len(results['graph_size']))
                  if results['density'][i] == density and results['k'][i] == k_ and results['dijkstra_accuracy'][i] is not None]
            ys = [results['dijkstra_accuracy'][i] for i in range(len(results['graph_size']))
                  if results['density'][i] == density and results['k'][i] == k_ and results['dijkstra_accuracy'][i] is not None]
            if xs:
                plt.plot(xs, ys, marker='o', label=f"Dijkstra: dens={density}, k={k_}")
    plt.xlabel("Graph Size (nodes)")
    plt.ylabel("Accuracy (fraction correct)")
    plt.title("k-Relaxation Dijkstra: Accuracy vs Graph Size")
    plt.ylim(0, 1.05)
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # 3) space
    plt.figure(figsize=(10, 5))
    for density in sorted(set(results['density'])):
        for k_ in sorted(set(results['k'])):
            xs = [results['graph_size'][i] for i in range(len(results['graph_size']))
                  if results['density'][i] == density and results['k'][i] == k_ and results['dijkstra_space'][i] is not None]
            ys = [results['dijkstra_space'][i] for i in range(len(results['graph_size']))
                  if results['density'][i] == density and results['k'][i] == k_ and results['dijkstra_space'][i] is not None]
            if xs:
                plt.plot(xs, ys, marker='o', label=f"Dijkstra: dens={density}, k={k_}")
    plt.xlabel("Graph Size (nodes)")
    plt.ylabel("Space (bytes, approx.)")
    plt.title("k-Relaxation Dijkstra: Space Usage vs Graph Size")
    plt.ylim(bottom=0, top=max(ys)*1.1 if ys else 1000)
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # --- Bellman-Ford Plots ---
    # 1) time 
    plt.figure(figsize=(10, 5))
    for density in sorted(set(results['density'])):
        for k_ in sorted(set(results['k'])):
            xs = [results['graph_size'][i] for i in range(len(results['graph_size']))
                  if results['density'][i] == density and results['k'][i] == k_ and results['bellman_ford_time'][i] is not None]
            ys = [results['bellman_ford_time'][i] for i in range(len(results['graph_size']))
                  if results['density'][i] == density and results['k'][i] == k_ and results['bellman_ford_time'][i] is not None]
            if xs:
                plt.plot(xs, ys, marker='o', label=f"Bellman-Ford: dens={density}, k={k_}")
    plt.xlabel("Graph Size (nodes)")
    plt.ylabel("Time (s)")
    plt.title("k-Relaxation Bellman-Ford: Time vs Graph Size")
    plt.ylim(bottom=0, top=max(ys)*1.1 if ys else 0.05)
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # 2) accuracy 
    plt.figure(figsize=(10, 5))
    for density in sorted(set(results['density'])):
        for k_ in sorted(set(results['k'])):
            xs = [results['graph_size'][i] for i in range(len(results['graph_size']))
                  if results['density'][i] == density and results['k'][i] == k_ and results['bellman_ford_accuracy'][i] is not None]
            ys = [results['bellman_ford_accuracy'][i] for i in range(len(results['graph_size']))
                  if results['density'][i] == density and results['k'][i] == k_ and results['bellman_ford_accuracy'][i] is not None]
            if xs:
                plt.plot(xs, ys, marker='o', label=f"Bellman-Ford: dens={density}, k={k_}")
    plt.xlabel("Graph Size (nodes)")
    plt.ylabel("Accuracy (fraction correct)")
    plt.title("k-Relaxation Bellman-Ford: Accuracy vs Graph Size")
    plt.ylim(0, 1.05)
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # 3) space 
    plt.figure(figsize=(10, 5))
    for density in sorted(set(results['density'])):
        for k_ in sorted(set(results['k'])):
            xs = [results['graph_size'][i] for i in range(len(results['graph_size']))
                  if results['density'][i] == density and results['k'][i] == k_ and results['bellman_ford_space'][i] is not None]
            ys = [results['bellman_ford_space'][i] for i in range(len(results['graph_size']))
                  if results['density'][i] == density and results['k'][i] == k_ and results['bellman_ford_space'][i] is not None]
            if xs:
                plt.plot(xs, ys, marker='o', label=f"Bellman-Ford: dens={density}, k={k_}")
    plt.xlabel("Graph Size (nodes)")
    plt.ylabel("Space (bytes, approx.)")
    plt.title("k-Relaxation Bellman-Ford: Space Usage vs Graph Size")
    plt.ylim(bottom=0, top=max(ys)*1.1 if ys else 1000)
    plt.legend()
    plt.grid(True)
    plt.show()


# Example Usage
# experiment_2()







#############################################################################################################################
# PART 3
#############################################################################################################################

def dijkstra_P3(graph, source):

    # initialize distances and previous pointers.
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    dist[source] = 0

    # build a list of Node objects for every vertex.
    nodes = [Item(v, dist[v]) for v in graph]
    heap = Heap(nodes)

    # process vertices until the heap is empty.
    while not heap.is_empty():
        current_node = heap.extract_min()
        u = current_node.value

        # relax edges from u.
        for v, weight in graph[u].items():
            alt = dist[u] + weight
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                # update the key in the heap.
                heap.decrease_key(v, alt)
                
    return dist, prev

def all_pairs_dijkstra(graph):

    all_dist = {}
    all_prev = {}
    
    for node in graph:
        dist, prev = dijkstra_P3(graph, node)
        all_dist[node] = dist
        all_prev[node] = prev
    
    return all_dist, all_prev






def bellman_P3(graph, source):

    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    dist[source] = 0

    # create a list of all edges
    edges = []
    for u in graph:
        for v, weight in graph[u].items():
            edges.append((u, v, weight))

    # relax all edges |V| - 1 times
    for _ in range(len(graph) - 1):
        for u, v, weight in edges:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                prev[v] = u

    # check for negative-weight cycles
    for u, v, weight in edges:
        if dist[u] + weight < dist[v]:
            raise ValueError("graph contains a negative weight cycle")
    
    return dist, prev

def all_pairs_bellman(graph):

    all_dist = {}
    all_prev = {}

    for node in graph:
        dist, prev = bellman_P3(graph, node)
        all_dist[node] = dist
        all_prev[node] = prev
    
    return all_dist, all_prev





""""
For all-pairs shortest paths on dense graphs:

Dijkstra 
  - single run: 
        In a dense graph, there are many edges — almost every pair of vertices is connected. 
        So, E≈V^2, which give us O(V^2).

  - all-pairs: 
        Run Dijkstra from each vertex, giving O(V) x O(V^2) = O(V^3).

Bellman-Ford 
  - single run:
        For dense graphs, E = O(V^2), and since bellman complexity is O(VE), it becomes O(V^3) per run.

  - all-pairs: 
        Running bellman from each vertex gives us O(V) x O(V^3) = O(V^4).

    So, for dense graphs:
  - all-pairs Dijkstra is O(V^3).
  - all-pairs Bellman-Ford is O(V^4).

"""












#############################################################################################################################
# below is code template for part 4
# part 4 A*
#############################################################################################################################

def A_Star_part4(graph, start, goal, heuristic):
    """
    Implements the A* algorithm to find the shortest path from start to goal.
    
    :param graph: Dictionary where keys are nodes and values are lists of (neighbor, weight) pairs.
    :param start: The starting node.
    :param goal: The target node.
    :param heuristic: Dictionary mapping nodes to heuristic values (estimated cost to goal).
    :return: A tuple (cameFrom dictionary, shortest path cost).
    """
    # The set of discovered nodes that may need to be (re-)expanded.
    openSet = [(heuristic[start], start)]  # Priority queue (min-heap)
    
    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path.
    cameFrom = {}
    
    # gScore stores the cost from start to each node, defaulting to infinity.
    gScore = {node: float('inf') for node in graph.get_graph()}
    gScore[start] = 0
    
    # fScore[n] = gScore[n] + h(n), representing our best guess at total cost.
    fScore = {node: float('inf') for node in graph.get_graph()}
    fScore[start] = heuristic[start]


    #graph adjacency lists and weights
    neighbours = graph.get_graph()
    
        
    while openSet:
        # Get the node with the lowest fScore value
        _, current = heapq.heappop(openSet)
        
        
        if current == goal:
            
            path = []
            while current in cameFrom:
                
                path.append(current)
                current = cameFrom[current]
            path.append(start)
            path.reverse()
            
            return cameFrom, (path, gScore[goal])
        
        for neighbor in neighbours[current]:
            
            
            weight = graph.get_weight(current,neighbor)
            tentative_gScore = gScore[current] + weight
            
            if tentative_gScore < gScore[neighbor]:
                # This path to neighbor is better than any previous one.
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = tentative_gScore + heuristic[neighbor]
                heapq.heappush(openSet, (fScore[neighbor], neighbor))
    
    return cameFrom, ([], float('inf'))  # No path found





#############################################################################################################################
# below is code template for part 5
# part 5 A*
#############################################################################################################################
def A_Star(graph, start, goal, heuristic):
    
    # The set of discovered nodes that may need to be (re-)expanded.
    openSet = [(heuristic[start], start)]  # Priority queue (min-heap)
    
    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path.
    cameFrom = {}
    
    # gScore stores the cost from start to each node, defaulting to infinity.
    gScore = {node: float('inf') for node in graph.get_graph()}
    gScore[start] = 0
    
    # fScore[n] = gScore[n] + h(n), representing our best guess at total cost.
    fScore = {node: float('inf') for node in graph.get_graph()}
    fScore[start] = heuristic[start]


    #graph adjacency lists and weights
    neighbours = graph.get_graph()
    
        
    while openSet:
        # Get the node with the lowest fScore value
        _, current = heapq.heappop(openSet)
        
        
        if current == goal:
            
            path = []
            while current in cameFrom:
                
                path.append(current)
                current = cameFrom[current]
            path.append(start)
            path.reverse()
            
            return (path, gScore[goal])
        
        for neighbor in neighbours[current]:
            
            
            weight = graph.get_weight(current,neighbor)
            tentative_gScore = gScore[current] + weight
            
            if tentative_gScore < gScore[neighbor]:
                # This path to neighbor is better than any previous one.
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = tentative_gScore + heuristic[neighbor]
                heapq.heappush(openSet, (fScore[neighbor], neighbor))
    
    return ([], float('inf'))  # No path found
        

def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    # Radius of Earth in kilometers (change to 3958.8 for miles)
    R = 6371  
    distance = R * c

    return distance  # Distance in kilometers

def generate_graph(filename, filename2):
    graph = UnDirectedWeightedGraph()

    with open(filename, 'r') as london_connections, open(filename2, 'r') as london_stations :
        
        next(london_stations)
        adjacency_list = []
        
        for line in london_stations:
            parts = line.strip().split(',')
            graph.add_coordinate(parts[0], parts[1], parts[2])

        locations = graph.get_coordinates()

        next(london_connections)  # Skip the first line (header)
        
        for line in london_connections:
            parts = line.strip().split(',')
            node1 = parts[0]
            node2 = parts[1]

            lat1, lon1 = locations[node1]
            lat2,lon2 = locations[node2]
            
            weight = haversine(float(lat1),float(lon1),float(lat2),float(lon2))
            adjacency_list.append((node1, node2, weight))
    
    for i in range(len(adjacency_list)):
        
        node1, node2, weight = adjacency_list[i]
        graph.add_node(node1)
        graph.add_node(node2)
        
        graph.add_edge(node1, node2, weight)

    return graph

def heuristic_calulater(graph, dst):


    heuristic = {}
    coordinates =  graph.get_coordinates()
    for src in graph.get_graph():

        lat1, lon1 = coordinates[src]
        lat2,lon2 = coordinates[dst]
            
        heuristic[src] = haversine(float(lat1),float(lon1),float(lat2),float(lon2))

    return heuristic


   


def dijkstra(graphInput, source, target):
    graph = graphInput.get_graph()
    
    distances = {node: float('inf') for node in graph}
    predecessors = {node: None for node in graph}  # To reconstruct paths
    distances[source] = 0
    heap = Heap([])
    
    # Insert all nodes with their distances
    for node in graph:
        heap.insert(Item(node, distances[node]))
    
    while not heap.is_empty():
        u = heap.extract_min().value  # Node with min distance
        
        # Early exit if we've found the target
        if u == target:
            break
        
        for v in graph[u]:
            new_distance = distances[u] + graphInput.get_weight(u, v)
            if new_distance < distances[v]:
                distances[v] = new_distance
                predecessors[v] = u  # Update predecessor
                heap.decrease_key(v, new_distance)  # Update priority
    
    # Reconstruct the path from source to target
    path = []
    current_node = target
    
    # If target is unreachable, return an empty path
    if distances[target] == float('inf'):
        return distances, []
    
    # Backtrack from target to source
    while current_node is not None:
        path.append(current_node)
        current_node = predecessors[current_node]
    
    path.reverse()  # Reverse to get source -> target order
    
    return distances, path



def all_pairs(Graph):
    list_of_nodes = []
    all_pair = []
    graph = Graph.get_graph()

    for node in graph:
        list_of_nodes.append(node)

    for i in range(len(list_of_nodes)):
        for j in range(i+1, len(list_of_nodes)):
            all_pair.append((list_of_nodes[i],list_of_nodes[j]))

    return all_pair








#############################################################################################################################
# PART 5 experiment function
#############################################################################################################################

def experiment_5():
    graph = generate_graph("london_connections.csv", "london_stations.csv")
     
    
    all_possible_pairs = all_pairs(graph)

    run_times_dijkstra =[]
    run_times_A_star =[]

    for i in range(len(all_possible_pairs)):
        src, dst = all_possible_pairs[i]
        
        
        start = timeit.default_timer()
        # calculate heuristic
        heuristic = heuristic_calulater(graph, dst)
        # Run A*
        A_Star(graph, src, dst, heuristic)
        stop = timeit.default_timer()
        run_times_A_star.append(stop-start)


        start = timeit.default_timer()
        dijkstra(graph, src, dst)
        stop = timeit.default_timer()
        run_times_dijkstra.append(stop-start)

    total_time_A_star = 0
    total_time_dijkstra = 0
    for i in range(len(run_times_A_star)):
        total_time_A_star += run_times_A_star[i]
        total_time_dijkstra += run_times_dijkstra[i]

    mean_A_star = total_time_A_star/len(run_times_A_star)
    mean_dijkstra = total_time_dijkstra/ len(run_times_dijkstra)
    draw_plot(run_times_A_star,mean_A_star, "A star algorithm",run_times_dijkstra, mean_dijkstra, "Dijkstra algorithm","London subway System")
        
    return 

# Example Usage
# experiment_5()






    