import pytest
from qiskit import transpile
from qiskit_aer import AerSimulator

# Adjust the import path
from src.grover_circuit import (
    create_grover_circuit,
    calculate_dynamic_iterations,
    calculate_optimal_iterations,
)

# Use AerSimulator for running the circuits
simulator = AerSimulator(method="automatic")

TEST_CASES = [
    {"num_qubits": 3, "targets": "101"},
    {"num_qubits": 4, "targets": "1100"},
    {"num_qubits": 2, "targets": "11"},
]

@pytest.mark.parametrize("case", TEST_CASES)
def test_grover_finds_target_state(case):
    num_qubits = case["num_qubits"]
    targets = case["targets"]
    shots = 1024

    grover_circuit = create_grover_circuit(num_qubits, targets, measure=True)

    t_circuit = transpile(grover_circuit, simulator)
    job = simulator.run(t_circuit, shots=shots)
    result = job.result()
    counts = result.get_counts(grover_circuit)

    most_frequent = max(counts, key=counts.get)
    assert most_frequent == targets
    probability = counts.get(targets, 0) / shots
    assert probability > 0.7


def test_grover_multiple_targets():
    num_qubits = 3
    targets = ["101", "010"]
    shots = 1024

    circuit = create_grover_circuit(num_qubits, targets, measure=True)
    t_circuit = transpile(circuit, simulator)
    result = simulator.run(t_circuit, shots=shots).result()
    counts = result.get_counts(circuit)

    prob_sum = sum(counts.get(t, 0) for t in targets) / shots
    assert prob_sum > 0.7
    assert all(counts.get(t, 0) > 0 for t in targets)


def test_grover_circuit_invalid_input():
    with pytest.raises(ValueError, match="Number of qubits must be at least 1"):
        create_grover_circuit(0, "")

    with pytest.raises(ValueError, match="must match num_qubits"):
        create_grover_circuit(3, "10")
    with pytest.raises(ValueError, match="must match num_qubits"):
        create_grover_circuit(3, "1011") # Too long


def test_dynamic_iterations_reduce_depth():
    """Adaptive iteration count should not exceed optimal iterations."""
    num_qubits = 3
    target_state = "101"

    optimal = calculate_optimal_iterations(num_qubits)
    dynamic = calculate_dynamic_iterations(num_qubits, target_state, threshold=0.8)

    assert dynamic <= optimal

    shots = 1024
    circuit = create_grover_circuit(
        num_qubits,
        target_state,
        iterations=dynamic,
        measure=True,
    )
    t_circuit = transpile(circuit, simulator)
    result = simulator.run(t_circuit, shots=shots).result()
    counts = result.get_counts(circuit)
    target_prob = counts.get(target_state, 0) / shots

    assert target_prob > 0.7
