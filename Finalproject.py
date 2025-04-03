import heapq

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
        
        for neighbor, weight in graph[current]:
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

    def adjacent_nodes(self, node):
        return self.adj[node]

    def add_node(self, node):
        self.adj[node] = []

    def add_edge(self, node1, node2, weight):
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
        self.weights[(node1, node2)] = weight

    def get_weight(self, node1, node2):
        
        return self.weights[(node1, node2)]
        

    def get_graph(self,):
        return self.adj
        

def generate_graph(list):
    s = DirectedWeightedGraph()
    for i in range(len(list)):
        
        node1, node2, weight = list[i]
        s.add_node(node1)
        s.add_node(node2)
        s.add_edge(node1, node2, weight)

    return s.get_graph()

def parse_connections(filename):
    with open(filename, 'r') as file:
        next(file)  # Skip the first line (header)
        adjacency_list = []
        
        for line in file:
            parts = line.strip().split(',')
            node1 = parts[0]
            node2 = parts[1]
            adjacency_list.append((node1, node2))
    
    return adjacency_list  # Return outside the loop
print(parse_connections("london_connections.csv"))
