import streamlit as st

# --------------------------------------------------
# Function to calculate maximum profit
# --------------------------------------------------
def calculate_max_profit(total_time):
    
    # Step 1: Building details (time needed & earnings)
    buildings = {
        "T": {"build_time": 5, "earning_per_unit": 1500},
        "P": {"build_time": 4, "earning_per_unit": 1000},
        "C": {"build_time": 10, "earning_per_unit": 2000}
    }

    # Step 2: DP table
    # dp[t] = (max_profit_at_time_t, list_of_solutions)
    # solution format → (theatre_count, pub_count, commercial_count)
    dp = [(-1, []) for _ in range(total_time + 1)]

    # Base case: at time 0, profit is 0 and no buildings are built
    dp[0] = (0, [(0, 0, 0)])

    # Step 3: Try building at every possible time
    for current_time in range(total_time + 1):

        current_profit, current_solutions = dp[current_time]

        # Skip invalid states
        if current_profit == -1:
            continue

        # Step 4: Try each building type
        for building_type in buildings:

            build_time = buildings[building_type]["build_time"]
            earning = buildings[building_type]["earning_per_unit"]

            # Check if building fits in remaining time
            if current_time + build_time <= total_time:

                # Time left after construction
                remaining_time = total_time - (current_time + build_time)

                # Profit earned by this building
                new_profit = current_profit + (remaining_time * earning)

                # Step 5: Update solution counts
                for solution in current_solutions:
                    t_count, p_count, c_count = solution

                    if building_type == "T":
                        new_solution = (t_count + 1, p_count, c_count)
                    elif building_type == "P":
                        new_solution = (t_count, p_count + 1, c_count)
                    else:
                        new_solution = (t_count, p_count, c_count + 1)

                    # Step 6: Update DP table
                    next_time = current_time + build_time
                    stored_profit, stored_solutions = dp[next_time]

                    # Case 1: Found better profit
                    if new_profit > stored_profit:
                        dp[next_time] = (new_profit, [new_solution])

                    # Case 2: Found same profit → add solution
                    elif new_profit == stored_profit:
                        if new_solution not in stored_solutions:
                            stored_solutions.append(new_solution)

    # Step 7: Find maximum profit from all times
    max_profit = 0
    best_solutions = []

    for profit, solutions in dp:
        if profit > max_profit:
            max_profit = profit
            best_solutions = solutions
        elif profit == max_profit:
            best_solutions.extend(solutions)

    # Remove duplicate solutions
    best_solutions = list(set(best_solutions))

    return max_profit, best_solutions


# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------
st.set_page_config(page_title="Max Profit Problem", layout="centered")

st.title("🏗️ Max Profit Problem")
st.write(
    "Find the best way to build Theatres (T), Pubs (P), and Commercial Parks (C) "
    "to earn the maximum profit within the given time."
)

# User input
total_time = st.number_input(
    "Enter total available time units:",
    min_value=1,
    step=1
)

# Button click
if st.button("Calculate Maximum Profit"):

    profit, solutions = calculate_max_profit(total_time)

    st.success(f"💰 Maximum Profit: ${profit}")

    st.subheader("✅ Optimal Building Combinations")

    for index, (t, p, c) in enumerate(solutions, start=1):
        st.write(f"**Solution {index}:** T: {t}  P: {p}  C: {c}")



