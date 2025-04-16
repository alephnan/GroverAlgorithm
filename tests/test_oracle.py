import pytest
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator # Add AerSimulator import

# Adjust the import path based on your project structure
# If tests/ is at the same level as src/, this should work:
from src.oracle import create_oracle

# Get the statevector simulator backend using AerSimulator
simulator = AerSimulator(method='statevector') # Updated simulator instantiation

def test_oracle_marks_target_state():
    """Test if the oracle correctly applies a negative phase to the target state."""
    num_qubits = 3
    target_state_binary = "101" # Target state |101>
    target_state_decimal = int(target_state_binary, 2)

    # Create the oracle
    oracle = create_oracle(num_qubits, target_state_binary)

    # Create a test circuit: initialize to target state, apply oracle
    qc = QuantumCircuit(num_qubits)

    # --- Method 1: Initialize directly to target state (requires reversing binary string for Qiskit) ---
    # initial_state = np.zeros(2**num_qubits)
    # initial_state[target_state_decimal] = 1
    # qc.initialize(initial_state, range(num_qubits))

    # --- Method 2: Create uniform superposition and check phase flip relative to others ---
    qc.h(range(num_qubits)) # Start from uniform superposition

    # Apply the oracle
    qc.append(oracle, range(num_qubits))
    qc.save_statevector() # Explicitly save statevector

    # Simulate the circuit to get the final statevector
    # Need to transpile for the simulator if using MCZ or other composite gates
    t_qc = transpile(qc, simulator)
    job = simulator.run(t_qc) # Remove shots=1
    result = job.result()
    statevector = result.get_statevector()

    # Verification for Method 2 (Superposition):
    # Check if the amplitude of the target state has a flipped phase relative to others.
    # All initial amplitudes are 1/sqrt(N). Target should become -1/sqrt(N).
    initial_amplitude = 1 / np.sqrt(2**num_qubits)
    target_amplitude = statevector[target_state_decimal]

    # Check phase of target state (should be negative relative to others)
    assert np.isclose(target_amplitude, -initial_amplitude), \
        f"Oracle did not flip phase for target state {target_state_binary}. Amplitude: {target_amplitude}"

    # Check phase of a non-target state (should remain positive)
    non_target_state_decimal = 0 # e.g., |000>
    if non_target_state_decimal == target_state_decimal:
        non_target_state_decimal = 1 # Choose a different one if target is 0

    non_target_amplitude = statevector[non_target_state_decimal]
    assert np.isclose(non_target_amplitude, initial_amplitude), \
        f"Oracle incorrectly changed phase for non-target state {non_target_state_decimal}. Amplitude: {non_target_amplitude}"

def test_oracle_invalid_input():
    """Test if the oracle raises ValueError for mismatched input lengths."""
    num_qubits = 3
    target_state_binary_short = "10" # Incorrect length
    target_state_binary_long = "1011" # Incorrect length

    with pytest.raises(ValueError, match="must match num_qubits"):
        create_oracle(num_qubits, target_state_binary_short)

    with pytest.raises(ValueError, match="must match num_qubits"):
        create_oracle(num_qubits, target_state_binary_long)

# Add more tests as needed, e.g., for edge cases like 1 qubit 