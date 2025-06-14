import numpy as np
from typing import Sequence
from qiskit import QuantumCircuit, ClassicalRegister

# Use explicit relative imports
from .oracle import create_oracle
from .diffuser import create_diffuser

def calculate_optimal_iterations(num_qubits: int, num_solutions: int = 1) -> int:
    """Calculate the optimal number of Grover iterations.

    Supports multiple marked states via ``num_solutions``.
    """
    if num_qubits < 1:
        return 0
    if num_solutions < 1 or num_solutions > 2 ** num_qubits:
        raise ValueError("num_solutions must be between 1 and 2**num_qubits")

    n_states = 2 ** num_qubits
    theta = np.arcsin(np.sqrt(num_solutions / n_states))
    iterations = int(np.round(np.pi / (4 * theta) - 0.5))
    return max(1, iterations)

def create_grover_circuit(
    num_qubits: int,
    target_states_binary: str | Sequence[str],
    iterations: int | None = None,
    measure: bool = True,
) -> QuantumCircuit:
    """Creates the full Grover algorithm circuit.

    Args:
        num_qubits: The total number of qubits for the search.
        target_states_binary: A binary string or list of binary strings
            representing the target state(s).
        iterations: The number of times to apply the Oracle-Diffuser block.
                    If None, calculates the optimal number based on the number
                    of target states.
        measure: If True, adds measurement gates at the end.

    Returns:
        A QuantumCircuit object representing the Grover algorithm.

    Raises:
        ValueError: If num_qubits is less than 1 or any target state has the
            wrong length.
    """
    if num_qubits < 1:
        raise ValueError("Number of qubits must be at least 1.")

    if isinstance(target_states_binary, str):
        target_states = [target_states_binary]
    else:
        target_states = list(target_states_binary)

    if not target_states:
        raise ValueError("At least one target state must be provided.")
    for state in target_states:
        if len(state) != num_qubits:
            raise ValueError(
                f"Length of target_state_binary ({len(state)}) must match num_qubits ({num_qubits})."
            )

    # Determine the number of iterations
    if iterations is None:
        num_iterations = calculate_optimal_iterations(num_qubits, len(target_states))
    else:
        num_iterations = iterations

    # Create components
    oracle = create_oracle(num_qubits, target_states)
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