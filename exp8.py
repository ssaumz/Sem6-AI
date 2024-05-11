from itertools import permutations

class State:
    def __init__(self, block_condition):
        self.misplaced_blocks = 100
        self.state = block_condition
        self.parent_state = None
        self.move = "INITIAL STATE"


    def backtrack(self, sequence):
        if self.parent_state is None:
            return sequence
        sequence.insert(0, self.parent_state)
        return self.parent_state.backtrack(sequence)


class BlockWorld:
    def __init__(self,
                 initial_condition: State,
                 goal_condition:State
                 ):
        self.initial_state = initial_condition
        self.goal_state = goal_condition
        self.blocks = []
        for block_condition in initial_condition.state:
            for block in block_condition:
                if block not in self.blocks:
                    self.blocks.append(block)

        self.initial_state.misplaced_blocks = self.heuristic_function(initial_condition)
        self.states = [self.initial_state]
        self.explored_states = []

    # ON CONDITION
    def on(self, above, below, current_state: State):
        for block in current_state.state:
            if block[0]==above and block[1]==below:
                return True

        return False

    # CLEAR CONDITION
    def clear(self, block, current_state:State):
        for state in current_state.state:
            if state[1] == block:
                return False

        return True

    # ACTION Move(b, x, y)
    def stack(self, b, y, current_state: State):
        new_state = []
        for block_state in current_state.state:
            if block_state[0] == b:
                new_state.append([b, y])
            else:
                new_state.append(block_state)
        return new_state

#   ACTION MoveToTable(b,x)
    def move_to_table(self, b, current_state: State):
        new_state = []
        for block_state in current_state.state:
            if block_state[0] == b:
                new_state.append([b, "Table"])
            else:
                new_state.append(block_state)
        return new_state

#     SIMPLE HEURISTIC FUNCTION
    def heuristic_function(self, current_state: State):
        misplaced_blocks = 0
        for m in range(0, 3):
            for n in range(0, 2):
                if current_state.state[m][n] != self.goal_state.state[m][n]:
                    misplaced_blocks += 1

        return misplaced_blocks

    def next_possible_move(self, current_state: State):
        possible_moves = []
        movable_blocks = []
        for block in self.blocks:
            if self.clear(block, current_state):
                movable_blocks.append(block)

        for movable_block in movable_blocks:
            for block in self.blocks:
                precondition_for_moving_to_table = (self.on(movable_block, block, current_state)
                                                    and self.clear(movable_block, current_state)
                                                    and movable_block != block and block != "Table")
                if precondition_for_moving_to_table:
                    possible_state = State(self.move_to_table(movable_block, current_state))
                    possible_state.move = f"Moving {movable_block} to Table"
                    possible_state.parent_state = current_state
                    possible_state.misplaced_blocks = self.heuristic_function(possible_state)
                    possible_moves.append(possible_state)

            stackable_block = [x for x in self.blocks if x!=movable_block]
            permutation_list = list(permutations(stackable_block, 2))
            for x, y in permutation_list:
                precondition_for_stacking = (self.on(movable_block, x, current_state)
                                             and self.clear(movable_block, current_state)
                                             and self.clear(y, current_state) and movable_block != x
                                             and movable_block != y and x != y)
                if precondition_for_stacking:
                    possible_state = State(self.stack(movable_block, y, current_state))
                    possible_state.move = f"Placing {movable_block} on {y}"
                    possible_state.parent_state = current_state
                    possible_state.misplaced_blocks = self.heuristic_function(possible_state)
                    possible_moves.append(possible_state)

        return possible_moves

    def print_solution(self, answer):
        for solution_state in answer:
            print("---------------------------------")
            print(solution_state.move)
            for block_position in solution_state.state:
                print(f"{block_position[0]} on {block_position[1]}")

    def planning(self):
        while True:
            if not len(self.states):
                print("GOAL STATE CANNOT BE REACHED")
                print("-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-")
                break
            current_state = self.states.pop(0)
            if self.heuristic_function(current_state) == 0:
                answer_sequence = current_state.backtrack([current_state])
                self.print_solution(answer_sequence)
                print("GOAL STATE REACHED")
                print("-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-")
                break

            for next_possible_state in self.next_possible_move(current_state):
                if next_possible_state not in self.explored_states:
                    self.states.append(next_possible_state)

            self.explored_states.append(current_state)

            self.states.sort(key=lambda x: x.misplaced_blocks)


initial_stack_condition = []
goal_stack_condition = []
print("Enter the initial state as 'A on Table' or 'B on C'")
for i in range(0, 3):
    condition = input().split(" on ")
    initial_stack_condition.append(condition)

print("\nEnter the goal state as 'A on Table' or 'B on C'")
for j in range(0, 3):
    condition = input().split(" on ")
    goal_stack_condition.append(condition)

initial_state = State(initial_stack_condition)
goal_state = State(goal_stack_condition)

block_world_problem = BlockWorld(initial_state, goal_state)
block_world_problem.planning()
