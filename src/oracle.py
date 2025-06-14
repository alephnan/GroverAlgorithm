from typing import Iterable, Sequence
from qiskit import QuantumCircuit


def _single_state_oracle(num_qubits: int, target_state_binary: str) -> QuantumCircuit:
    """Create an oracle that flips the phase of a single computational basis state."""
    if len(target_state_binary) != num_qubits:
        raise ValueError(
            f"Length of target_state_binary ({len(target_state_binary)}) must match num_qubits ({num_qubits})."
        )

    oracle = QuantumCircuit(num_qubits, name=f"Oracle_{target_state_binary}")

    # Flip qubits corresponding to '0' so the multi-controlled Z targets |1...1>
    reversed_target = target_state_binary[::-1]
    zero_indices = [i for i, bit in enumerate(reversed_target) if bit == "0"]
    if zero_indices:
        oracle.x(zero_indices)

    if num_qubits == 1:
        oracle.z(0)
    elif num_qubits == 2:
        oracle.cz(0, 1)
    else:
        controls = list(range(num_qubits - 1))
        target = num_qubits - 1
        oracle.h(target)
        oracle.mcx(controls, target)
        oracle.h(target)

    if zero_indices:
        oracle.x(zero_indices)

    return oracle


def create_oracle(num_qubits: int, target_states_binary: str | Sequence[str]) -> QuantumCircuit:
    """Create an oracle that marks one or more computational basis states.

    Args:
        num_qubits: Total number of qubits in the circuit.
        target_states_binary: Either a single binary string or a sequence of
            binary strings representing the target state(s). Each string's length
            must match ``num_qubits``.

    Returns:
        QuantumCircuit implementing the oracle for all target states.

    Raises:
        ValueError: If any target state's length does not match ``num_qubits``
            or if ``target_states_binary`` is empty.
    """

    if isinstance(target_states_binary, str):
        target_states: Iterable[str] = [target_states_binary]
    else:
        target_states = list(target_states_binary)

    if not target_states:
        raise ValueError("At least one target state must be provided.")

    for state in target_states:
        if len(state) != num_qubits:
            raise ValueError(
                f"Length of target_state_binary ({len(state)}) must match num_qubits ({num_qubits})."
            )

    oracle_circuit = QuantumCircuit(num_qubits, name="Oracle")

    for state in target_states:
        single = _single_state_oracle(num_qubits, state)
        oracle_circuit.compose(single, range(num_qubits), inplace=True)

    return oracle_circuit
