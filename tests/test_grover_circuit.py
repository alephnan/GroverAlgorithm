import pytest
from qiskit import transpile
from qiskit_aer import AerSimulator

# Adjust the import path
from src.grover_circuit import create_grover_circuit

# Get the QASM simulator backend using AerSimulator
simulator = AerSimulator(method='automatic')

# Define test parameters (can be parameterized further with pytest.mark.parametrize)
TEST_CASES = [
    {"num_qubits": 3, "target_state": "101"},
    {"num_qubits": 4, "target_state": "1100"},
    # Add more test cases, perhaps edge cases like 2 qubits
    {"num_qubits": 2, "target_state": "11"},
]

@pytest.mark.parametrize("case", TEST_CASES)
def test_grover_finds_target_state(case):
    """Test if Grover's algorithm finds the correct target state with high probability."""
    num_qubits = case["num_qubits"]
    target_state = case["target_state"]
    shots = 1024 # Number of times to run the measurement

    # Create the Grover circuit (using optimal iterations by default)
    grover_circuit = create_grover_circuit(num_qubits, target_state, measure=True)

    # Transpile for the simulator
    t_circuit = transpile(grover_circuit, simulator)

    # Run the simulation
    job = simulator.run(t_circuit, shots=shots)
    result = job.result()
    counts = result.get_counts(grover_circuit)

    # Find the outcome with the highest count
    # Note: Qiskit counts keys seem to be big-endian in this setup.
    # We compare the target_state directly to the key from counts.
    most_frequent_outcome = max(counts, key=counts.get)
    # target_state_qiskit_endian = target_state[::-1] # No reversal needed

    # Assert that the most frequent outcome is the target state
    assert most_frequent_outcome == target_state, \
        f"Grover did not find target {target_state}. Most frequent key: {most_frequent_outcome}. Counts: {counts}"

    # Optionally, assert that the target state has a high probability
    # Check the target state key directly in counts dict
    target_probability = counts.get(target_state, 0) / shots
    # Theoretical probability isn't always 1, especially for small N or non-optimal iterations
    # A lower bound check is more robust
    assert target_probability > 0.7, \
        f"Probability of target state {target_state} was too low ({target_probability:.3f}). Counts: {counts}"

def test_grover_circuit_invalid_input():
    """Test input validation for the Grover circuit creation."""
    # Test invalid number of qubits
    with pytest.raises(ValueError, match="Number of qubits must be at least 1"):
        create_grover_circuit(0, "")

    # Test mismatched target state length
    with pytest.raises(ValueError, match="must match num_qubits"):
        create_grover_circuit(3, "10") # Too short
    with pytest.raises(ValueError, match="must match num_qubits"):
        create_grover_circuit(3, "1011") # Too long 