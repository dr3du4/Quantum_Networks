import pandas as pd
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit,  transpile, assemble
import  qiskit_aer
# Read the initial state from CSV file
initial_state_df = pd.read_csv('initial_state.csv')
initial_state = initial_state_df.iloc[0]['state']  # Assuming the CSV has a column named 'state'

# Quantum program setup
q = QuantumRegister(3, 'q')
c0 = ClassicalRegister(1, 'c0')
c1 = ClassicalRegister(1, 'c1')
c2 = ClassicalRegister(1, 'c2')

# Creates the quantum circuit
teleport = QuantumCircuit(q, c0, c1, c2)

# Prepare the initial state for teleportation
if initial_state == '0':
    teleport.initialize([1, 0], q[0])
elif initial_state == '1':
    teleport.initialize([0, 1], q[0])

# Make the shared entangled state
teleport.h(q[1])
teleport.cx(q[1], q[2])

# Perform the Bell measurement on Alice's qubits
teleport.cx(q[0], q[1])
teleport.h(q[0])

# Measure Alice's qubits
teleport.measure(q[0], c0[0])
teleport.measure(q[1], c1[0])

# Bob applies the appropriate corrections
teleport.cx(q[1], q[2])
teleport.cz(q[0], q[2])

# Measure Bob's qubit
teleport.measure(q[2], c2[0])

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
result_df.to_csv('teleportation_results.csv', index=False)