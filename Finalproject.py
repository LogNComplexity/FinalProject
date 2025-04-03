import heapq
import math
from math import radians, cos, sin, asin, sqrt

def A_Star(graph, start, goal, heuristic):
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
    gScore = {node: float('inf') for node in graph}
    gScore[start] = 0
    
    # fScore[n] = gScore[n] + h(n), representing our best guess at total cost.
    fScore = {node: float('inf') for node in graph}
    fScore[start] = heuristic[start]


    #graph adjacency lists and weights
    neighbours = graph.get_graph()
    weights = graph.get_weights()    
    while openSet:
        # Get the node with the lowest fScore value
        _, current = heapq.heappop(openSet)
        
        if current == goal:
            # Reconstruct path
            path = []
            while current in cameFrom:
                path.append(current)
                current = cameFrom[current]
            path.append(start)
            path.reverse()
            return cameFrom, (path, gScore[goal])
        
        for neighbor in neighbours[current]:
            weight = weights[(current,neighbor)]
            tentative_gScore = gScore[current] + weight
            
            if tentative_gScore < gScore[neighbor]:
                # This path to neighbor is better than any previous one.
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = tentative_gScore + heuristic[neighbor]
                heapq.heappush(openSet, (fScore[neighbor], neighbor))
    
    return cameFrom, ([], float('inf'))  # No path found



# below is code template for part 5
class DirectedWeightedGraph:

    def __init__(self):
        self.adj = {}
        self.weights = {}
        self.coordinates = {}

    def adjacent_nodes(self, node):
        return self.adj[node]
    
    def add_coordinate(self,node, lat, lon):
        self.coordinates[node] = (lat,lon)

    def add_node(self, node):
        self.adj[node] = []

    def add_edge(self, node1, node2, weight):
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
        self.weights[(node1, node2)] = weight

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
    graph = DirectedWeightedGraph()

    with open(filename, 'r') as london_connections, open(filename2, 'r') as london_stations :
        
        next(london_stations)
        adjacency_list = []
        
        for line in london_stations:
            parts = line.strip().split(',')
            graph.add_coordinate[parts[0]] = (parts[1], parts[2])

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
    for src in graph.get_graph():

        lat1, lon1 = graph.get_coordinates()[src]
        lat2,lon2 = graph.get_coordinates()[dst]
            
        heuristic[src] = haversine(float(lat1),float(lon1),float(lat2),float(lon2))

    return heuristic



    