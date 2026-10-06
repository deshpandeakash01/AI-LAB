class EightPuzzleDFS:
    def __init__(self, start_state, goal_state):
        self.start_state = tuple(start_state)
        self.goal_state = tuple(goal_state)
        self.moves = {
            'UP': (-1, 0),
            'DOWN': (1, 0),
            'LEFT': (0, -1),
            'RIGHT': (0, 1)
        }
    def get_neighbors(self, state):
        neighbors = []
        blank_idx = state.index(0)
        row, col = blank_idx // 3, blank_idx % 3
        for move_name, (dr, dc) in self.moves.items():
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_blank_idx = new_row * 3 + new_col
                new_state = list(state)
                new_state[blank_idx], new_state[new_blank_idx] = new_state[new_blank_idx], new_state[blank_idx]
                neighbors.append((tuple(new_state), move_name))
        return neighbors
    def solve(self, max_depth=20):
        stack = [(self.start_state, [], 0)]
        visited = {self.start_state: 0}
        nodes_expanded = 0
        while stack:
            current_state, path, depth = stack.pop()
            nodes_expanded += 1
            if current_state == self.goal_state:
                return path, nodes_expanded
            if depth >= max_depth:
                continue
            for neighbor_state, move in reversed(self.get_neighbors(current_state)):
                # If state is unvisited OR found via a shorter/more efficient path
                if neighbor_state not in visited or depth + 1 < visited[neighbor_state]:
                    visited[neighbor_state] = depth + 1
                    stack.append((neighbor_state, path + [move], depth + 1))

        return None, nodes_expanded
    def print_board(self, state):
        for i in range(0, 9, 3):
            print(f"[{state[i]} {state[i+1]} {state[i+2]}]")
        print()
if __name__ == "__main__":
    start = (1, 2, 3, 
             4, 0, 5, 
             6, 7, 8)
    
    goal  = (1, 2, 3, 
             4, 5, 8, 
             6, 7, 0)

    puzzle = EightPuzzleDFS(start, goal)
    print("Initial State:")
    puzzle.print_board(start)
    print("Goal State:")
    puzzle.print_board(goal)
    max_depth_limit = 15
    print(f"Searching for solution using DFS (Depth Limit: {max_depth_limit})...")
    solution_path, total_nodes = puzzle.solve(max_depth=max_depth_limit)
    if solution_path is not None:
        print(f"Solution Found in {len(solution_path)} moves!")
        print(f"Moves taken: {' -> '.join(solution_path)}")
        print(f"Total nodes expanded: {total_nodes}")
    else:
        print(f" No solution found within a depth of {max_depth_limit} moves.")