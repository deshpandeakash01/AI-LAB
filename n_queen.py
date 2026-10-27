import random

N = 4  # Size of the board (4-Queens)

def get_cost(state):
    """Calculates number of attacking pairs of queens."""
    conflicts = 0
    for i in range(N):
        for j in range(i + 1, N):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def hill_climbing():
    # Initialize with a random board setup
    current_state = [random.randint(0, N - 1) for _ in range(N)]
    current_cost = get_cost(current_state)
    
    step = 0
    while True:
        print(f"\n--- STEP {step} ---")
        print(f"Current State: {current_state} (Cost: {current_cost})")
        print("Evaluating all neighboring states:")
        
        best_neighbor = list(current_state)
        best_cost = current_cost
        
        # Check every single possible neighbor state
        for col in range(N):
            for row in range(N):
                if row == current_state[col]:
                    continue  # Skip current queen position
                
                # Generate neighbor state by moving one queen
                neighbor = list(current_state)
                neighbor[col] = row
                neighbor_cost = get_cost(neighbor)
                
                # Print every generated neighbor state and its cost
                print(f"  Neighbor: {neighbor} -> Cost: {neighbor_cost}")
                
                # Keep track of the absolute best neighbor
                if neighbor_cost < best_cost:
                    best_cost = neighbor_cost
                    best_neighbor = neighbor
        if best_cost >= current_cost:
            if current_cost == 0:
                print(f"\n🎉 SUCCESS: Goal state {current_state} reached!")
                return True
            else:
                print(f"\n🛑 STUCK: Local optimum reached at {current_state}. Restarting...")
                return False
        current_state = best_neighbor
        current_cost = best_cost
        step += 1
success = False
while not success:
    success = hill_climbing()
