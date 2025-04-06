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




# below is code template for part 4
# part 4 A*
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


# below is code template for part 5
# part 5 A*
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




# part 5 experiment

def experiment5():
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

# Example usage
experiment5()






    