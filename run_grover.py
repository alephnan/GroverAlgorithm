import sys
import os
import argparse

# This allows importing modules from the 'src' package
script_dir = os.path.dirname(__file__) # This is the project root

# Add the project root directory to sys.path
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# Optional: Check if src exists (mainly for clarity
src_check_path = os.path.join(script_dir, 'src')
if not os.path.isdir(src_check_path):
    print(f"Error: 'src' directory not found in {script_dir}")
    sys.exit(1)

try:
    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import AerSimulator
    # Qiskit visualization requires matplotlib uncomment if you want to plot the histogram
    # from qiskit.visualization import plot_histogram
    # import matplotlib.pyplot as plt
except ImportError:
    print("Qiskit or Qiskit Aer is not installed.")
    print("Please install them using: pip install qiskit qiskit-aer")
    # print("For visualization, also install: pip install matplotlib")
    sys.exit(1)

try:
    # Import using the 'src.' prefix
    from src.grover_circuit import create_grover_circuit, calculate_optimal_iterations
except ImportError as e:
    print(f"Error importing from src: {e}")
    print("Make sure the 'src' directory exists in the project root and contains the necessary modules.")
    # print("Current sys.path:", sys.path) # Uncomment for debugging path issues
    sys.exit(1)

def run_simulation(n_qubits: int, marked_state_binary: str, shots: int = 1024):
    """
    Sets up and runs Grover's algorithm simulation for a given number of qubits
    and a marked state.
    """
    print(f"--- Running Grover's Algorithm ---")
    print(f"Number of qubits: {n_qubits}")
    print(f"Marked state: |{marked_state_binary}>")

    try:
        # Calculate optimal iterations (optional, create_grover_circuit does it)
        num_iterations = calculate_optimal_iterations(n_qubits)
        print(f"Optimal number of iterations: {num_iterations}")

        # Create Grover circuit (measure=True is default in create_grover_circuit now)
        grover_circuit = create_grover_circuit(
            num_qubits=n_qubits,
            target_state_binary=marked_state_binary,
            iterations=num_iterations,
            measure=True # Explicitly adding measure gates
        )

        # print("\nCircuit Diagram:")
        # print(grover_circuit.draw(output='text')) # Optional: print text diagram

    except ValueError as e:
        print(f"Error creating circuit: {e}")
        sys.exit(1)

    # Simulate
    print(f"\nSimulating circuit with {shots} shots...")
    simulator = AerSimulator()
    compiled_circuit = transpile(grover_circuit, simulator)
    job = simulator.run(compiled_circuit, shots=shots)
    result = job.result()
    counts = result.get_counts(compiled_circuit)

    print(f"\nSimulation Results (Counts):")
    # Sort counts for better readability (optional)
    sorted_counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
    print(sorted_counts)

    # Plot results (optional, requires matplotlib)
    # try:
    #     plot_histogram(counts, title=f"Grover Results ({n_qubits} qubits, target='{marked_state_binary}')")
    #     plt.show()
    # except NameError: # If matplotlib wasn't imported
    #     print("\n(Install matplotlib to see the histogram plot)")
    # except Exception as e:
    #     print(f"\nCould not display histogram plot: {e}")


    # Check if the marked state was found
    most_frequent_state = max(counts, key=counts.get)
    print(f"\nMost frequent measurement result: {most_frequent_state}")
    if most_frequent_state == marked_state_binary:
        print(f"Success! The marked state |{marked_state_binary}> was found with highest probability.")
    else:
        print(f"Marked state |{marked_state_binary}> was not the most frequent outcome.")
    print("----------------------------------")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Grover's Algorithm Simulation.")
    parser.add_argument(
        "-n", "--num_qubits", type=int, required=True,
        help="Number of qubits for the search."
    )
    parser.add_argument(
        "-m", "--marked_state", type=str, required=True,
        help="The binary string representing the state to search for (e.g., '101')."
    )
    parser.add_argument(
        "-s", "--shots", type=int, default=1024,
        help="Number of simulation shots (default: 1024)."
    )

    args = parser.parse_args()

    if len(args.marked_state) != args.num_qubits:
        parser.error(f"Length of marked_state ('{args.marked_state}', length {len(args.marked_state)}) "
                     f"must equal num_qubits ({args.num_qubits}).")

    if not all(c in '01' for c in args.marked_state):
         parser.error(f"marked_state ('{args.marked_state}') must be a binary string (containing only '0' or '1').")

    run_simulation(args.num_qubits, args.marked_state, args.shots) 