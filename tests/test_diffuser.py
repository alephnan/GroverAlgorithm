import pytest
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Adjust the import path based on your project structure
from src.diffuser import create_diffuser

# Get the statevector simulator backend using AerSimulator
simulator = AerSimulator(method='statevector')

def test_diffuser_on_uniform_superposition():
    """Test if the diffuser acts correctly on the uniform superposition state.

    Applying the diffuser D = 2|psi><psi| - I to the uniform superposition state
    |psi> = H^n |0>^n should result in the same state |psi> (up to global phase).
    """
    num_qubits = 3
    N = 2**num_qubits

    # 1. Create the expected initial state (uniform superposition)
    initial_qc = QuantumCircuit(num_qubits)
    initial_qc.h(range(num_qubits))
    initial_qc.save_statevector() # Explicitly save statevector
    t_initial_qc = transpile(initial_qc, simulator)
    job = simulator.run(t_initial_qc) # Remove shots=1, not needed for statevector
    initial_statevector = job.result().get_statevector()
    # Expected statevector: [1/sqrt(N), 1/sqrt(N), ..., 1/sqrt(N)]

    # 2. Create the diffuser
    diffuser = create_diffuser(num_qubits)

    # 3. Apply the diffuser to the uniform superposition state
    qc = QuantumCircuit(num_qubits)
    qc.h(range(num_qubits)) # Prepare |psi>
    qc.append(diffuser, range(num_qubits)) # Apply D
    qc.save_statevector() # Explicitly save statevector

    # Simulate the circuit
    t_qc = transpile(qc, simulator)
    job = simulator.run(t_qc) # Remove shots=1
    final_statevector = job.result().get_statevector()

    # 4. Verify that the final state is the same as the initial state (up to global phase)
    # We check if the absolute value of the inner product is close to 1.
    inner_product = np.vdot(initial_statevector.data, final_statevector.data)
    assert np.isclose(np.abs(inner_product), 1.0), \
        f"Diffuser did not preserve the uniform superposition state up to global phase.\n" \
        f"Initial: {initial_statevector}\nFinal: {final_statevector}\nInner Product: {inner_product}"

def test_diffuser_invalid_input():
    """Test if the diffuser raises ValueError for num_qubits < 1."""
    with pytest.raises(ValueError, match="Number of qubits must be at least 1"):
        create_diffuser(0)

# Add more tests if needed, e.g., testing the phase flip property for orthogonal states 