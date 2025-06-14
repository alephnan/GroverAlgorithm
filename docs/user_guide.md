# User Guide: Grover's Algorithm Implementation

## 1. Introduction

This guide explains how to use the Grover's algorithm implementation provided in this project. It covers importing the necessary components, creating the circuit, running simulations, and checking performance.

## 2. Prerequisites

Before using the code, ensure you have followed the setup instructions in the main `README.md` file, including:
- Cloning the repository.
- Creating and activating the Python virtual environment.
- Installing the required dependencies from `requirements.txt`.

## 3. Importing Components

The core functions for creating the Grover circuit and its components are located in the `src` directory. You can import them as follows:

```python
from src.oracle import create_oracle
from src.diffuser import create_diffuser
from src.grover_circuit import create_grover_circuit, calculate_optimal_iterations
from src.performance import print_performance_metrics # Optional for checking stats

# Qiskit imports for running simulations
from qiskit import transpile
from qiskit.providers.basic_provider import BasicSimulator
```

## 4. Creating the Grover Circuit

To create a Grover circuit, you need to specify the number of qubits and the target state (as a binary string).

```python
# Example: 3 qubits, target state |101>
num_qubits = 3
target_state = "101"

# Create the circuit (calculates optimal iterations automatically)
grover_circuit = create_grover_circuit(num_qubits, target_state, measure=True)

# You can also specify the number of iterations manually
# num_iterations = 1
# grover_circuit_manual_iter = create_grover_circuit(num_qubits, target_state, iterations=num_iterations, measure=True)

# Print the circuit (optional)
print(grover_circuit.draw(output='text'))
```

You can also provide multiple target states by passing a list of binary strings:

```python
target_states = ["101", "010"]
grover_multi = create_grover_circuit(num_qubits, target_states, measure=True)
```

## 5. Running the Simulation

You can simulate the circuit using Qiskit's simulators (like `qasm_simulator` for counts or `statevector_simulator` for the state vector).

```python
# Get a simulator backend
simulator = BasicSimulator().get_backend('qasm_simulator')
shots = 1024

# Transpile the circuit for the simulator (recommended)
t_circuit = transpile(grover_circuit, simulator)

# Run the simulation
job = simulator.run(t_circuit, shots=shots)
result = job.result()
counts = result.get_counts(grover_circuit)

print("\nSimulation Results (Counts):")
print(counts)

# Find the most probable outcome
most_probable_state = max(counts, key=counts.get)
print(f"\nMost probable state found: {most_probable_state}")
```

## 6. Checking Performance Metrics

If you want to check the circuit's depth and gate counts before running:

```python
from src.performance import print_performance_metrics

print("\nCircuit Performance:")
# Note: Metrics are based on the high-level circuit before transpilation
print_performance_metrics(grover_circuit)
```

## 7. Configuration (Optional)

Currently, the core parameters (number of qubits, target state) are passed directly to the functions. The `config/settings.yaml` file is available for future extensions, such as defining problem-specific parameters or simulation settings. 