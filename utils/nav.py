import heapq

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}  # node -> list of (neighbor, cost)

    def add_node(self, node):
        self.nodes.add(node)
        if node not in self.edges:
            self.edges[node] = []

    def add_edge(self, from_node, to_node, cost=1):
        self.add_node(from_node)
        self.add_node(to_node)
        self.edges[from_node].append((to_node, cost))
        # For undirected graph (store aisles), add reverse edge:
        self.edges[to_node].append((from_node, cost))


def dijkstra(graph, start, goal):
    """
    Find shortest path from start to goal using Dijkstra's algorithm.
    Returns path list and total cost.
    """
    queue = [(0, start, [])]
    visited = set()

    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in visited:
            continue

        path = path + [node]
        visited.add(node)

        if node == goal:
            return path, cost

        for neighbor, weight in graph.edges.get(node, []):
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, neighbor, path))

    return None, float('inf')


def heuristic(a, b):
    """
    Heuristic for A* (here using Manhattan distance for grid)
    a, b are (x, y) tuples
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(graph, start, goal, positions):
    """
    A* algorithm for shortest path in a graph.
    Args:
        graph: Graph object with edges
        start: start node
        goal: goal node
        positions: dict mapping node to (x, y) position for heuristic
    Returns:
        path list and total cost
    """
    queue = [(0 + heuristic(positions[start], positions[goal]), 0, start, [])]
    visited = set()

    while queue:
        (est_total_cost, cost_so_far, node, path) = heapq.heappop(queue)
        if node in visited:
            continue

        path = path + [node]
        visited.add(node)

        if node == goal:
            return path, cost_so_far

        for neighbor, weight in graph.edges.get(node, []):
            if neighbor not in visited:
                new_cost = cost_so_far + weight
                est = new_cost + heuristic(positions[neighbor], positions[goal])
                heapq.heappush(queue, (est, new_cost, neighbor, path))

    return None, float('inf')


if __name__ == "__main__":
    # Example usage:
    g = Graph()
    g.add_edge("entrance", "A1", 5)
    g.add_edge("A1", "A2", 7)
    g.add_edge("A2", "A3", 3)
    g.add_edge("A3", "checkout", 10)
    g.add_edge("A1", "A4", 2)

    positions = {
        "entrance": (0, 0),
        "A1": (5, 0),
        "A2": (12, 0),
        "A3": (15, 0),
        "A4": (5, 3),
        "checkout": (20, 0)
    }

    path, cost = dijkstra(g, "entrance", "checkout")
    print("Dijkstra path:", path, "cost:", cost)

    path, cost = astar(g, "entrance", "checkout", positions)
    print("A* path:", path, "cost:", cost)
