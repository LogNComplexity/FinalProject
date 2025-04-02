import heapq

def A_Star(graph, source, destination, heuristic):
    """
    Implements the A* algorithm to find the shortest path from source to destination.
    
    :param graph: Dictionary where keys are nodes and values are lists of (neighbor, weight) pairs.
    :param source: The starting node.
    :param destination: The target node.
    :param heuristic: Dictionary mapping nodes to heuristic values (estimated cost to goal).
    :return: A tuple (predecessor dictionary, shortest path cost).
    """
    # Priority queue (min-heap) for A* search
    pq = []
    heapq.heappush(pq, (0 + heuristic[source], source))  # (f = g + h, node)
    
    # Stores the cost from source to each node
    g_score = {node: float('inf') for node in graph}
    g_score[source] = 0
    
    # Stores the predecessors
    predecessor = {}
    
    while pq:
        _, current = heapq.heappop(pq)
        
        if current == destination:
            # Reconstruct path
            path = []
            while current in predecessor:
                path.append(current)
                current = predecessor[current]
            path.append(source)
            path.reverse()
            return predecessor, (path, g_score[destination])
        
        for neighbor, weight in graph[current]:
            tentative_g_score = g_score[current] + weight
            
            if tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic[neighbor]
                heapq.heappush(pq, (f_score, neighbor))
                predecessor[neighbor] = current
    
    return predecessor, ([], float('inf'))  # No path found
