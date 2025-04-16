from qiskit import QuantumCircuit

def create_diffuser(num_qubits: int) -> QuantumCircuit:
    """Creates the Grover diffuser (amplitude amplification) circuit.

    Also known as inversion about the mean.

    Args:
        num_qubits: The number of qubits for the diffuser.

    Returns:
        A QuantumCircuit object representing the diffuser.

    Raises:
        ValueError: If num_qubits is less than 1.
    """
    if num_qubits < 1:
        raise ValueError("Number of qubits must be at least 1.")

    diffuser_circuit = QuantumCircuit(num_qubits, name="Diffuser")

    # Apply Hadamard gates to all qubits
    diffuser_circuit.h(range(num_qubits))

    # Apply Pauli-X gates to all qubits
    diffuser_circuit.x(range(num_qubits))

    # Apply multi-controlled Z gate
    if num_qubits == 1:
        diffuser_circuit.z(0)
    elif num_qubits == 2:
        diffuser_circuit.cz(0, 1)
    else:
        controls = list(range(num_qubits - 1))
        target = num_qubits - 1
        # Implement MCZ using H gates and MCX
        diffuser_circuit.h(target)
        diffuser_circuit.mcx(controls, target)
        diffuser_circuit.h(target)

    # Apply Pauli-X gates to all qubits
    diffuser_circuit.x(range(num_qubits))

    # Apply Hadamard gates to all qubits
    diffuser_circuit.h(range(num_qubits))

    return diffuser_circuit 