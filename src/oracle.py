from qiskit import QuantumCircuit

def create_oracle(num_qubits: int, target_state_binary: str) -> QuantumCircuit:
    """Creates an oracle circuit that marks a specific computational basis state.

    Args:
        num_qubits: The total number of qubits in the circuit.
        target_state_binary: The binary string representing the target state to mark.
                             The length must match num_qubits.

    Returns:
        A QuantumCircuit object representing the oracle.

    Raises:
        ValueError: If the length of target_state_binary does not match num_qubits.
    """
    if len(target_state_binary) != num_qubits:
        raise ValueError(
            f"Length of target_state_binary ({len(target_state_binary)}) "
            f"must match num_qubits ({num_qubits})."
        )

    # Create the quantum circuit
    oracle_circuit = QuantumCircuit(num_qubits, name="Oracle")

    # Apply X gates to qubits corresponding to '0' in the target state
    # This flips the state so the multi-controlled Z gate targets |1...1>
    # REVERSE the string to match Qiskit's little-endian qubit order
    reversed_target = target_state_binary[::-1]
    zero_indices = [i for i, bit in enumerate(reversed_target) if bit == '0']
    if zero_indices:
        oracle_circuit.x(zero_indices)

    # Apply the multi-controlled Z gate
    # If num_qubits is 1, apply a Z gate
    # If num_qubits is 2, apply a CZ gate
    # Otherwise, use mcx with an auxiliary qubit or mcz if available
    if num_qubits == 1:
        oracle_circuit.z(0)
    elif num_qubits == 2:
        oracle_circuit.cz(0, 1)
    else:
        # Use multi-controlled Z gate (MCZ). Qiskit's standard gate library
        # might require decomposition for > 2 controls depending on the backend.
        # For simplicity here, we use mcz which might need synthesis/transpilation.
        controls = list(range(num_qubits - 1))
        target = num_qubits - 1
        # Implement MCZ using H gates and MCX
        oracle_circuit.h(target)
        oracle_circuit.mcx(controls, target)
        oracle_circuit.h(target)

    # Apply X gates again to restore the state
    if zero_indices:
        oracle_circuit.x(zero_indices)

    return oracle_circuit 