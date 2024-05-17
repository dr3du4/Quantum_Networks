import pandas as pd
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile, assemble
import qiskit_aer

# Read the initial state from CSV file
initial_state_df = pd.read_csv('initial_state_3.csv')
initial_states = initial_state_df.iloc[0].values  # Assuming the CSV has 3 columns, each for one qubit state

# Quantum program setup
q = QuantumRegister(9, 'q')  # 3 sets of 3 qubits for teleportation
c = ClassicalRegister(9, 'c')  # 3 sets of classical registers for measurement

# Creates the quantum circuit
teleport = QuantumCircuit(q, c)

# Prepare the initial states for teleportation
for i in range(3):
    state = initial_states[i]
    if state == '0':
        teleport.initialize([1, 0], q[3 * i])
    elif state == '1':
        teleport.initialize([0, 1], q[3 * i])


# Make the shared entangled state for each qubit
for i in range(3):
    teleport.h(q[3 * i + 1])
    teleport.cx(q[3 * i + 1], q[3 * i + 2])

    # Perform the Bell measurement on Alice's qubits
    teleport.cx(q[3 * i], q[3 * i + 1])
    teleport.h(q[3 * i])

    # Measure Alice's qubits
    teleport.measure(q[3 * i], c[3 * i])
    teleport.measure(q[3 * i + 1], c[3 * i + 1])

    # Bob applies the appropriate corrections
    teleport.cx(q[3 * i + 1], q[3 * i + 2])
    teleport.cz(q[3 * i], q[3 * i + 2])

    # Measure Bob's qubit
    teleport.measure(q[3 * i + 2], c[3 * i + 2])

# Shows gates of the circuit
simulator = qiskit_aer.Aer.get_backend('qasm_simulator')

# Transpile and assemble the circuit
transpiled_circuit = transpile(teleport, simulator)
qobj = assemble(transpiled_circuit, shots=1024)

# Run the algorithm
result = simulator.run(qobj).result()

counts = result.get_counts(teleport)
print('\nThe measured outcomes of the circuits are:', counts)

# Write the measurement results to a CSV file
result_df = pd.DataFrame(list(counts.items()), columns=['Measurement', 'Counts'])
result_df.to_csv('teleportation_3_results.csv', index=False)
