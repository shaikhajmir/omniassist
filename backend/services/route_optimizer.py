import networkx as nx

class RouteOptimizer:
    def __init__(self):
        # Create a mock city graph
        self.graph = nx.Graph()
        
        # Nodes: 1 to 5 (e.g. intersections/locations)
        # Edges have weights (e.g. distance or time)
        edges = [
            ("L1", "L2", 5),
            ("L1", "L3", 10),
            ("L2", "L4", 3),
            ("L3", "L4", 2),
            ("L4", "L5", 8),
            ("L2", "L5", 15)
        ]
        
        for u, v, w in edges:
            self.graph.add_edge(u, v, weight=w)

    def optimize_route(self, start_node, emergency_node):
        try:
            # Dijkstra's shortest path
            path = nx.shortest_path(self.graph, source=start_node, target=emergency_node, weight='weight')
            distance = nx.shortest_path_length(self.graph, source=start_node, target=emergency_node, weight='weight')
            return {"path": path, "distance": distance}
        except nx.NetworkXNoPath:
            return {"error": "No path found"}
        except nx.NodeNotFound:
            return {"error": "Invalid start or end node"}

route_optimizer = RouteOptimizer()
