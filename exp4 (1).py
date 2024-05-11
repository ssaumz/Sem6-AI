from collections import deque

class Graph:
    def __init__(self):
        self.graph_dict = {}

    def add_edge(self, node, neighbour):
        if node not in self.graph_dict:
            self.graph_dict[node] = []
        self.graph_dict[node].append(neighbour)

    def bfs(self, start_node, goal_node):
        visited = {start_node}
        queue = deque([(start_node, [start_node])])
        while queue:
            current_node, path = queue.popleft()
            print(f"Visiting node {current_node}, Path: {' -> '.join(path)}")
            if current_node == goal_node:
                print("Goal node reached!")
                return path
            for neighbour in self.graph_dict[current_node]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append((neighbour, path + [neighbour]))

    def dfs(self, start_node, goal_node):
        visited = set()
        stack = [(start_node, [start_node])]
        while stack:
            current_node, path = stack.pop()
            print(f"Visiting node {current_node}, Path: {' -> '.join(path)}")
            if current_node == goal_node:
                print("Goal node reached!")
                return path
            if current_node not in visited:
                visited.add(current_node)
                for neighbour in reversed(self.graph_dict[current_node]):
                    stack.append((neighbour, path + [neighbour]))

# Example usage:
if __name__ == "__main__":
    graph = Graph()
    # Input graph in matrix form
    matrix_size = int(input("Enter the size of the matrix: "))
    print("Enter the adjacency matrix (1 for connected, 0 for not connected):")
    matrix = [input().split() for _ in range(matrix_size)]
    # Construct graph from matrix
    for i in range(matrix_size):
        for j in range(matrix_size):
            if matrix[i][j] == '1':
                graph.add_edge(str(i), str(j))
    start_node = input("Enter the starting node for traversal: ")
    goal_node = input("Enter the goal node: ")
    print("\nBFS traversal:")
    bfs_path = graph.bfs(start_node, goal_node)
    print("BFS Path:", ' -> '.join(bfs_path))
    print("\nDFS traversal:")
    dfs_path = graph.dfs(start_node, goal_node)
    print("DFS Path:", ' -> '.join(dfs_path))
