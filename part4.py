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
