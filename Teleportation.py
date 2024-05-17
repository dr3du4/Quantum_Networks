from qiskit import *

from qiskit_aer import *
# Quantum program setup





# Creating registers

q = QuantumRegister(3, 'q')
c0 = ClassicalRegister(1, 'c0')
c1 = ClassicalRegister(1, 'c1')
c2 = ClassicalRegister(1, 'c2')

# Creates the quantum circuit
teleport = QuantumCircuit(q, c0,c1,c2)

# Make the shared entangled state
teleport.h(q[1])
# Bob checks the state of the teleported qubit
teleport.measure(q[2], c2[0])

# Shows gates of the circuit
simulator = Aer.get_backend('qasm_simulator')


# Transpile and assemble the circuit
transpiled_circuit = transpile(teleport, simulator)
qobj = assemble(transpiled_circuit, shots=1024)

# Run the algorithm
result = simulator.run(qobj).result()


counts = result.get_counts(teleport)
print('\nThe measured outcomes of the circuits are:', counts)