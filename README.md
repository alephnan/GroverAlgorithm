# Grover's Algorithm High-Performance Implementation

## Overview
This project implements Grover's Algorithm using Qiskit, focusing on performance optimization. The implementation demonstrates quantum speedup for unstructured search problems and is validated on simulators.

## Features
- Modular implementation: Oracle, Diffuser, and Grover Circuit
- Performance monitoring: gate count, depth, execution time

## Project Structure
```
grovers_algorithm_project/
├── src/
│   ├── __init__.py
│   ├── oracle.py
│   ├── diffuser.py
│   ├── grover_circuit.py
├── tests/
│   ├── __init__.py
│   ├── test_oracle.py
│   ├── test_diffuser.py
│   ├── test_grover_circuit.py
├── docs/
│   ├── design.md
│   ├── user_guide.md
|
├── notebooks/
│   ├── grover_demo2.ipynb
├── requirements.txt
└── README.md

```

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/alephnan/GroverAlgorithm.git
cd GroversAlgorithm
```

### 2. Create and activate a Python virtual environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run tests
```bash
pytest
```

## Usage

There are two main ways to run the Grover's algorithm simulation:

### 1. Command-Line Interface (CLI)

Use the `run_grover.py` script located in the project root. This script allows you to specify the number of qubits, the target state, and the number of simulation shots.

**Basic Syntax:**
```bash
python run_grover.py -n <num_qubits> -m <target_state_binary> [-s <shots>]
```

**Arguments:**
- `-n`, `--num_qubits`: (Required) The total number of qubits for the search.
- `-m`, `--marked_state`: (Required) The binary string representing the state to search for (e.g., '101'). The length must match `num_qubits`.
- `-s`, `--shots`: (Optional) The number of times the simulation is run to gather statistics (default: 1024).

**Example:**
To run a simulation with 3 qubits searching for the state `|101>`:
```bash
python run_grover.py -n 3 -m 101
```

The Python API also supports searching for multiple states by passing a list of
binary strings to `create_grover_circuit`.

To see all options:
```bash
python run_grover.py --help
```

### 2. Jupyter Notebook

A demonstration notebook is available in the `notebooks/` directory.

1.  Ensure you have Jupyter Notebook or JupyterLab installed (`pip install notebook` or `pip install jupyterlab`).
2.  Start the Jupyter server from your project root directory:
    ```bash
    jupyter notebook
    # or
    jupyter lab
    ```
3.  Navigate to the `notebooks/` folder in the Jupyter interface.
4.  Open `grover_demo.ipynb`.
5.  Run the cells in the notebook sequentially to see the algorithm in action, including visualizations.

## Contributing
- Follow security and code quality guidelines
- Run tests and security scans before submitting PRs

## License
MIT 