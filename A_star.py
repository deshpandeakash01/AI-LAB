import heapq

GOAL = "123456780"
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def get_heuristic(state, choice):
    """Calculates heuristic cost based on user preference."""
    # Choice 1: Manhattan Distance (highly efficient)
    if choice == 1:
        dist = 0
        for i, tile in enumerate(state):
            if tile != '0':
                g_r, g_c = divmod(GOAL.index(tile), 3)
                c_r, c_c = divmod(i, 3)
                dist += abs(g_r - c_r) + abs(g_c - c_c)
        return dist
        
    # Choice 2: Misplaced Tiles (counts tiles out of position)
    elif choice == 2:
        count = 0
        for i in range(9):
            if state[i] != '0' and state[i] != GOAL[i]:
                count += 1
        return count
    return 0

def print_board(state, step_num):
    print(f"--- Step {step_num} ---")
    for i in range(0, 9, 3):
        row = [tile if tile != '0' else ' ' for tile in state[i:i+3]]
        print(f"| {' | '.join(row)} |")
    print()

def solve_puzzle(start, heuristic_choice):
    h_cost = get_heuristic(start, heuristic_choice)
    queue = [(h_cost, 0, start, [start])]
    visited = {start}

    while queue:
        _, g, state, path = heapq.heappop(queue)

        if state == GOAL:
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
                    f = (g + 1) + get_heuristic(next_state, heuristic_choice)
                    heapq.heappush(queue, (f, g + 1, next_state, path + [next_state]))


initial_board = "123046758" 

print("Select Heuristic Function:")
print("1. Manhattan Distance")
print("2. Misplaced Tiles")
choice = int(input("Enter choice (1 or 2): "))

solve_puzzle(initial_board, choice)
