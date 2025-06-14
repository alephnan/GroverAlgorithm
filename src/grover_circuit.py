import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, transpile
from qiskit_aer import AerSimulator

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


def calculate_dynamic_iterations(
    num_qubits: int,
    target_state_binary: str,
    threshold: float = 0.95,
    max_iterations: int | None = None,
) -> int:
    """Determine the number of iterations adaptively using simulation.

    This function simulates the Grover circuit after each iteration and
    stops when the probability of measuring the target state exceeds the
    given ``threshold``. It returns the number of iterations required or
    ``max_iterations`` if the threshold is not reached.
    """
    if num_qubits < 1:
        raise ValueError("Number of qubits must be at least 1.")
    if len(target_state_binary) != num_qubits:
        raise ValueError(
            f"Length of target_state_binary ({len(target_state_binary)}) "
            f"must match num_qubits ({num_qubits})."
        )

    if max_iterations is None:
        max_iterations = calculate_optimal_iterations(num_qubits)

    oracle = create_oracle(num_qubits, target_state_binary)
    diffuser = create_diffuser(num_qubits)

    # Prepare initial superposition
    current_circuit = QuantumCircuit(num_qubits)
    current_circuit.h(range(num_qubits))

    simulator = AerSimulator(method="statevector")
    target_index = int(target_state_binary, 2)

    for iteration in range(1, max_iterations + 1):
        current_circuit.append(oracle, range(num_qubits))
        current_circuit.append(diffuser, range(num_qubits))

        test_circuit = current_circuit.copy()
        test_circuit.save_statevector()
        t_circ = transpile(test_circuit, simulator)
        state = simulator.run(t_circ).result().get_statevector()
        probability = abs(state[target_index]) ** 2

        if probability >= threshold:
            return iteration

    return max_iterations

def create_grover_circuit(
    num_qubits: int,
    target_state_binary: str,
    iterations: int | None = None,
    measure: bool = True,
    adaptive: bool = False,
    threshold: float = 0.95,
) -> QuantumCircuit:
    """Creates the full Grover algorithm circuit.

    Args:
        num_qubits: The total number of qubits for the search.
        target_state_binary: The binary string representing the target state.
        iterations: The number of times to apply the Oracle-Diffuser block.
                    If None, calculates the optimal number for a single target
                    or uses ``adaptive`` mode if enabled.
        measure: If True, adds measurement gates at the end.
        adaptive: If True, determine the number of iterations dynamically based
                   on ``threshold``.
        threshold: Success probability threshold used for adaptive iteration
                   count.

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
        if adaptive:
            num_iterations = calculate_dynamic_iterations(
                num_qubits,
                target_state_binary,
                threshold=threshold,
            )
        else:
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