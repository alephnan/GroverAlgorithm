from qiskit import QuantumCircuit

def get_circuit_depth(circuit: QuantumCircuit) -> int:
    """Calculate the depth of a quantum circuit.

    Args:
        circuit: The QuantumCircuit object.

    Returns:
        The depth of the circuit.
    """
    # Decompose the circuit first to get an accurate depth based on basis gates
    # This might be computationally intensive for large circuits.
    # Consider passing a QuantumInstance or Backend to transpile against specific gates.
    # decomposed_circuit = transpile(circuit, basis_gates=['u', 'cx']) # Example
    # return decomposed_circuit.depth()
    # For now, return depth without decomposition
    return circuit.depth()

def get_gate_counts(circuit: QuantumCircuit) -> dict[str, int]:
    """Count the occurrences of each gate type in a quantum circuit.

    Args:
        circuit: The QuantumCircuit object.

    Returns:
        A dictionary where keys are gate names (str) and values are counts (int).
    """
    # Similar to depth, decomposition affects counts.
    # decomposed_circuit = transpile(circuit, basis_gates=['u', 'cx']) # Example
    # return decomposed_circuit.count_ops()
    # For now, return counts without decomposition
    return circuit.count_ops()

def print_performance_metrics(circuit: QuantumCircuit):
    """Prints the depth and gate counts for a given circuit."""
    depth = get_circuit_depth(circuit)
    counts = get_gate_counts(circuit)

    print(f"Circuit Performance Metrics:")
    print(f"- Depth: {depth}")
    print(f"- Gate Counts: {counts}")
    # Add more metrics as needed 