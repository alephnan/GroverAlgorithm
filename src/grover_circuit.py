import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister

# Use explicit relative imports
from .oracle import create_oracle
from .diffuser import create_diffuser

def calculate_optimal_iterations(num_qubits: int) -> int:
    """Calculate the optimal number of Grover iterations for a single target state."""
    if num_qubits < 1:
        return 0
    if num_qubits == 2: # Special case for N=4 it's known that for N=4 (2 qubits), exactly 1 iteration is optimal.
        return 1
    amplitude = np.sqrt(2**num_qubits)
    # The formula is approx (pi/4) * sqrt(N/M), where N=2^n, M=1
    iterations = int(np.round((np.pi / 4.0) * amplitude))
    return max(1, iterations) # Need at least 1 iteration

def create_grover_circuit(
    num_qubits: int,
    target_state_binary: str,
    iterations: int | None = None,
    measure: bool = True
) -> QuantumCircuit:
    """Creates the full Grover algorithm circuit.

    Args:
        num_qubits: The total number of qubits for the search.
        target_state_binary: The binary string representing the target state.
        iterations: The number of times to apply the Oracle-Diffuser block.
                    If None, calculates the optimal number for a single target.
        measure: If True, adds measurement gates at the end.

    Returns:
        A QuantumCircuit object representing the Grover algorithm.

    Raises:
        ValueError: If num_qubits is less than 1 or target_state_binary length mismatch.
    """
    if num_qubits < 1:
        raise ValueError("Number of qubits must be at least 1.")
    if len(target_state_binary) != num_qubits:
        raise ValueError(
            f"Length of target_state_binary ({len(target_state_binary)}) "
            f"must match num_qubits ({num_qubits})."
        )

    # Determine the number of iterations
    if iterations is None:
        num_iterations = calculate_optimal_iterations(num_qubits)
    else:
        num_iterations = iterations

    # Create components
    oracle = create_oracle(num_qubits, target_state_binary)
    diffuser = create_diffuser(num_qubits)

    # Create main circuit
    grover_circuit = QuantumCircuit(num_qubits, name="Grover")

    # Add classical register for measurement if needed
    if measure:
        classical_register = ClassicalRegister(num_qubits, name="c")
        grover_circuit.add_register(classical_register)

    # 1. Initialization: Apply H gates to all qubits
    grover_circuit.h(range(num_qubits))
    grover_circuit.barrier()

    # 2. Grover Iterations: Apply Oracle and Diffuser repeatedly
    for _ in range(num_iterations):
        grover_circuit.append(oracle, range(num_qubits))
        grover_circuit.barrier()
        grover_circuit.append(diffuser, range(num_qubits))
        grover_circuit.barrier()

    # 3. Measurement (optional)
    if measure:
        grover_circuit.measure(range(num_qubits), classical_register)

    return grover_circuit 