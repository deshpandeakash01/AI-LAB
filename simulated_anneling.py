import random
import math
N = 8  # 8-Queens problem
def get_cost(state):
    """Calculates number of mutually attacking pairs of queens."""
    conflicts = 0
    for i in range(N):
        for j in range(i + 1, N):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts
def simulated_annealing():
    # 1. Initialize random state, high temperature, and cooling rate
    current_state = [random.randint(0, N - 1) for _ in range(N)]
    current_cost = get_cost(current_state)
    
    T = 100.0          # Initial Temperature
    cooling_rate = 0.95 # Alpha parameter to cool down
    threshold = 0.01   # Temperature stopping limit
    step = 0
    print(f"Initial State: {current_state} | Initial Conflicts: {current_cost}\n")
    
    while T > threshold:
        if current_cost == 0:
            print(f"\n🎉 SUCCESS: Found goal state {current_state} in {step} steps!")
            return True
            
        step += 1
        print(f"\n--- STEP {step} (Current Temp: {T:.2f}) ---")
        print(f"Current State: {current_state} (Cost: {current_cost})")
        
        # 2. Pick a random column and a random different row to make a neighbor state
        random_col = random.randint(0, N - 1)
        random_row = random.randint(0, N - 1)
        while random_row == current_state[random_col]:
            random_row = random.randint(0, N - 1)
            
        neighbor_state = list(current_state)
        neighbor_state[random_col] = random_row
        neighbor_cost = get_cost(neighbor_state)
        
        # Print the generated state evaluation details
        print(f"Generated Neighbor State: {neighbor_state} (Cost: {neighbor_cost})")
        
        # 3. Calculate Energy Delta (ΔE)
        delta_E = neighbor_cost - current_cost
        print(f"Delta E (Neighbor Cost - Current Cost): {delta_E}")
        
        # 4. Decision logic
        if delta_E < 0:
            # Better state -> Always accept
            current_state = neighbor_state
            current_cost = neighbor_cost
            print("Decision: Move ACCEPTED (Neighbor is better).")
        else:
            # Worse state -> Calculate probability to accept it anyway
            acceptance_prob = math.exp(-delta_E / T)
            random_val = random.random()
            print(f"Acceptance Probability: {acceptance_prob:.4f} | Random Roll: {random_val:.4f}")
            
            if random_val < acceptance_prob:
                current_state = neighbor_state
                current_cost = neighbor_cost
                print(" Decision: Move ACCEPTED (Worse state accepted to escape local minimum trap).")
            else:
                print("Decision: Move REJECTED. Staying at current state.")
                
        # 5. Cool down the temperature
        T *= cooling_rate
        
    print(f"\nTIMEOUT: Reached freezing point. Final state found: {current_state} with cost {current_cost}")
    return current_cost == 0

# Run the algorithm with a restart loop to ensure it successfully finds a global solution
success = False
attempt = 1
while not success:
    print(f"=== RUN ATTEMPT {attempt} ===")
    success = simulated_annealing()
    attempt += 1
    print("\n" + "="*50 + "\n")
