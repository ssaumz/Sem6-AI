import heapq

class PuzzleNode:
    def __init__(self, state, parent=None, move=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.g = g  # cost from start
        self.h = h  # heuristic cost

    def f(self):
        return self.g + self.h

    def __lt__(self, other):
        return self.f() < other.f()

def h_cost(state):
    """Calculate heuristic cost (Manhattan distance)."""
    global goal_state
    misplaced_tiles = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != goal_state[i][j] and state[i][j]!=0:
                misplaced_tiles += 1
    return misplaced_tiles

def get_successors(node):
    """Generate successor nodes."""
    successors = []
    global goal_state
    state = node.state
    i, j = next((i, j) for i in range(3) for j in range(3) if state[i][j] == 0)
    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ni, nj = i + di, j + dj
        if 0 <= ni < 3 and 0 <= nj < 3:
            new_state = [row[:] for row in state]
            new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
            successors.append(PuzzleNode(new_state, parent=node, move=(ni, nj), g=node.g + 1,h=h_cost(new_state)))
    return successors

def reconstruct_path(node):
    """Reconstruct the path from the initial state to the goal state."""
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]

def a_star(start_state, goal_state):
    open_list = []
    global result_states
    closed_set = set()

    start_node = PuzzleNode(start_state, g=0, h=h_cost(start_state))
    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node.state == goal_state:
            return reconstruct_path(current_node)

        closed_set.add(tuple(map(tuple, current_node.state)))

        for successor in get_successors(current_node):
            if tuple(map(tuple, successor.state)) in closed_set:
                continue

            if successor not in open_list or successor.f() < heapq.heappop(open_list).f():
                result_states.append(successor)
                heapq.heappush(open_list, successor)

    return None

def print_solution(solution):
    for i, state in enumerate(solution):
        print(f"Step {i}:")
        if i==0:
            g=0
            h=h_cost(state)
            f=g+h
            print(f"f(n)=h(n)+g(n)={h}+{g}={f}")
        for s in result_states:
            if s.state == state:
                print(f"f(n)=h(n)+g(n)={s.h}+{s.g}={s.f()}")
        for row in state:
            print(" ".join(map(str, row)))
        print()

def get_input(prompt):
    while True:
        try:
            input_data = input(prompt).strip().split(",")
            state = [list(map(int, input_data[i:i+3])) for i in range(0, len(input_data), 3)]
            if len(state) != 3 or any(len(row) != 3 for row in state):
                raise ValueError("Invalid input. Please enter 9 numbers separated by commas.")
            return state
        except ValueError as e:
            print(e)

def print_state_space_tree(start_state, goal_state):
    open_list = []
    start_node = PuzzleNode(start_state, g=0, h=h_cost(start_state))
    heapq.heappush(open_list, start_node)
    
    while open_list:
        current_node = heapq.heappop(open_list)
        print(f"Current State (f(n) = {current_node.f()}, h(n) = {current_node.h}, g(n) = {current_node.g}):")
        if current_node.state == goal_state:
            print("Goal State Reached!")
            return
        
        for successor in get_successors(current_node):
            heapq.heappush(open_list, successor)
            print(f"Child State (f(n) = {successor.f()}, h(n) = {successor.h}, g(n) = {successor.g}))")

if __name__ == "__main__":
    print("Enter the initial state (9 numbers separated by commas, use 0 for the blank space):")
    initial_state = get_input("Initial state: ")

    print("Enter the goal state (9 numbers separated by commas, use 0 for the blank space):")
    goal_state = get_input("Goal state: ")

    print("State Space Tree:")
    print_state_space_tree(initial_state, goal_state)
    result_states = []
    solution = a_star(initial_state, goal_state)
    if solution:
        print("\nSolution found:")
        print_solution(solution)
    else:
        print("No solution found.")