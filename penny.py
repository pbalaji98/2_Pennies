#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from qiskit import *
import matplotlib.pyplot as plt


# # Initial state

# In[18]:


### statevector simulation #####
circ = QuantumCircuit(2)
circ.h(0)
circ.h(1)
circ.save_statevector()

# Transpile for simulator
simulator = Aer.get_backend('aer_simulator')
circ = transpile(circ, simulator)

# Run and get statevector
result = simulator.run(circ).result()
statevector = result.get_statevector(circ)


# In[19]:


statevector


# In[20]:


### measurement simulation #####
circ = QuantumCircuit(2)
circ.h(0)
circ.h(1)
circ.measure_all()

# Transpile for simulator
simulator = Aer.get_backend('aer_simulator')
circ = transpile(circ, simulator)

# Run and get statevector
result = simulator.run(circ).result()
counts = result.get_counts(circ)
plt.hist(counts)


# # Grover iterate

# In[ ]:


def find_oracle(state_to_amplify):
	circ = QuantumCircuit(3)
	if (state_to_amplify == "11"):
		circ.ccx(2, 1, 0)
		return Operator(circ)
	if (state_to_amplify == "00")
		circ.x(1); circ.x(2); 
		circ.ccx(2, 1, 0)
		circ.x(1); circ.x(2)
		return Operator(circ)
	if (state_to_amplify == "01")
		circ.x(2); 
		circ.ccx(2, 1, 0)
		circ.x(2)
		return Operator(circ)
	if (state_to_amplify == "10")
		circ.x(1); 
		circ.ccx(2, 1, 0)
		circ.x(1)
		return Operator(circ)
 
# In[3]:


# Gets the reflection gate R that reflects across the ancilla qubit
def find_reflection():
    circ = QuantumCircuit(3)
    circ.z(0)
    return Operator(circ)

# Gets the iterate U*R*U^-1*R
def find_iterate(state_to_amplify):
    circ = QuantumCircuit(3)
    Uop = find_oracle(state_to_amplify)
    Rop = find_reflection()
    circ.append(Rop, [0,1,2])
    circ.append(Uop, [0,1,2])
    circ.append(Rop, [0,1,2])
    circ.append(Uop, [0,1,2])
    return Operator(circ)


# Function is obsolete for now, using find_iterate instead?
# note cur_state is a circuit
# state_to_amplify is an integer between 0 and 3 representing one of the basis states
# def grover_iterate(cur_state, state_to_amplify): 
#     oracle = find_oracle(state_to_amplify)
#     preparation = cur_state.gates()
#     projection = matrix_to_gate([[1,0,0,0],[0,-1,0,0],[0,0,-1,0],[0,0,0,-1]])
    
#     cur_state.append(oracle)
#     cur_state.append(preparation)
#     cur_state.append(projection)
#     cur_state.append(preparation.inverse())
    
#     return cur_state

# Takes in the current state the player fed it, and then returns a circuit with OAA applied
# The ancilla qubit from OAA is still attached here (it hasn't been measured yet), as the 0 register
def oblivious_amplification(curr_state, state_to_amplify, num_iterations):
	oracle = find_oracle(state_to_amplify); ancillary = QuantumRegister(1, 'ancillary')
    iterate = find_iterate(state_to_amplify)
	new_state = ancillary + curr_state
	#new_state.append(oracle, [2,1,0])
    new_state.append(oracle, [0,1,2])
    for i in range(num_iterations):
        new_state.append(iterate, [0,1,2])
    #Reset ancilla qubit
    new_state.append(oracle, [0,1,2])
    #new_state.measure([0],[0])
    return new_state

# Appends some easy scrambling gates (XH) to the start of the amplification circuit
def soft_scramble(curr_state):
    for i in range(curr_state.width):
        curr_state.x(i)
        curr_state.h(i)
    return curr_state



# # Gate sets for player

# In[ ]:




