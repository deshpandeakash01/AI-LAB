import heapq
GOAL = "123456780"
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]
def manhattan(state):
    dist = 0
    for i, tile in enumerate(state):
        if tile != '0':
            g_r, g_c = divmod(GOAL.index(tile), 3)
            c_r, c_c = divmod(i, 3)
            dist += abs(g_r - c_r) + abs(g_c - c_c)
    return dist
def print_board(state, step_num):
    """Prints the state nicely formatted as a 3x3 grid."""
    print(f"--- Step {step_num} ---")
    for i in range(0, 9, 3):
        row = [tile if tile != '0' else ' ' for tile in state[i:i+3]]
        print(f"| {row[0]} | {row[1]} | {row[2]} |")
    print()
def solve_puzzle(start):
    queue = [(manhattan(start), 0, start, [start])]
    visited = {start}
    while queue:
        _, g, state, path = heapq.heappop(queue)
        if state == GOAL:
            # Loop through and display every recorded intermediate state
            for step_num, current_state in enumerate(path):
                print_board(current_state, step_num)
            print(f" Success! Solved in {len(path) - 1} steps.")
            return
        blank = state.index('0')
        r, c = divmod(blank, 3)

        for dr, dc in MOVES:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                neighbor = nr * 3 + nc
                arr = list(state)
                arr[blank], arr[neighbor] = arr[neighbor], arr[blank]
                next_state = "".join(arr)

                if next_state not in visited:
                    visited.add(next_state)
                    f = (g + 1) + manhattan(next_state)
                    heapq.heappush(queue, (f, g + 1, next_state, path + [next_state]))
initial_board = "123405786" 
solve_puzzle(initial_board)
