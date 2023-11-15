.. _services:

Services
========

Qsimov Quantum Computing S.L. provides the following services for quantum computation.

Extra qubits service
--------------------

This service calculates the extra ancilla qubits needed for the quantum circuit to genenerate the superposition based on the specified parameters.

**Required parameters:**

- Metric information:

	- `metric` (str): The metric to be used in the quantum computation.
	
- Reference state information:

		- `n_qubits` (int): Number of qubits in the quantum circuit. 
		- `state` (int): Integer representation of the reference quantum state. 
	
	Or
	
		- `state_bin` (str): Binary representation of the reference quantum state.
	
- Distance information:

		- `distances` (list): List of strings distances for specific distances.
	
	Or
	
		- `min_range` (str): Minimum range for distance calculations (included).
		- `max_range` (str): Maximum range for distance calculations (included).
		
	And
	
		- `with_nan` (bool): Specify whether NaN (0/0) values are inclided in the superposition.
		
		
**Example Usage:**

.. code-block:: python

	from qsimov_cloud_client import QsimovCloudClient

	# Initialize QsimovCloudClient with your access token
	client = QsimovCloudClient("your_access_token")

	# Set parameters for the service
	client.set_metric("ample")
	client.set_state(num_qubits=5, state=2)
	client.set_range(["1/10", "5/10"])
	client.can_have_nan(True)
	client.set_ancilla_mode("clean")

	# Calculate the number of extra qubits
	n_extra_qubits = client.calculate_extra_qubits()

	# Access the result
	print("The number of extra ancilla qubits needed in:", n_extra_qubits)

.. note::

   Make sure to replace "your_access_token" with your actual Qsimov access token.
		
Distances range service
-----------------------

This service calculates the minimum and maximum distance/similarity range based on the metric and reference state.

**Required parameters:**

- Metric information:

	- `metric` (str): The metric to be used in the quantum computation.
	
- Reference state information:

		- `n_qubits` (int): Number of qubits in the quantum circuit. 
		- `state` (int): Integer representation of the reference quantum state. 
	
	Or
	
		- `state_bin` (str): Binary representation of the reference quantum state.
	
		
**Example Usage:**

.. code-block:: python

	from qsimov_cloud_client import QsimovCloudClient

	# Initialize QsimovCloudClient with your access token
	client = QsimovCloudClient("your_access_token")

	# Set parameters for the service
	client.set_metric("ample")
	client.set_state(state_bin="10110")

	# Calculate min and max range
	min_range, max_range = client.calculate_extra_qubits()

	# Access the result
	print("The min range and max range is:", min_range, max_range)
	
.. note::

   Make sure to replace "your_access_token" with your actual Qsimov access token.


Circuit Service
---------------

This service genenerates the superposition quantum circuit in OpenQASM :cite:`cross2017open` based on the specified parameters. Additionally, it calculates the extra number of qubits required and the total number of superposed states.

**Required parameters:**

- Metric information:

	- `metric` (str): The metric to be used in the quantum computation.
	
- Reference state information:

		- `n_qubits` (int): Number of qubits in the quantum circuit. 
		- `state` (int): Integer representation of the reference quantum state. 
	
	Or
	
		- `state_bin` (str): Binary representation of the reference quantum state.
	
- Distance information:

		- `distances` (list): List of strings distances for specific distances.
	
	Or
	
		- `min_range` (str): Minimum range for distance calculations (included).
		- `max_range` (str): Maximum range for distance calculations (included).
		
	And
	
		- `with_nan` (bool): Specify whether NaN (0/0) values are inclided in the superposition.
		
**Example Usage:**

.. code-block:: python

	from qsimov_cloud_client import QsimovCloudClient

	# Initialize QsimovCloudClient with your access token
	client = QsimovCloudClient("your_access_token")

	# Set parameters for the service
	client.set_metric("hamming")
	client.set_state(num_qubits=5, state=2)
	client.set_distances(["1", "3"])
	client.can_have_nan(False)
	client.set_ancilla_mode("noancilla")

	# Generate a quantum circuit
	circuit_superposition = client.generate_circuit()

	# Access the result
	print("The resulting circuit in qasm is:", circuit_superposition.get_qasm_code())

.. note::

   Make sure to replace "your_access_token" with your actual Qsimov access token.


.. warning::
   
   Using the "noancilla" ancilla mode may result in exponential growth in the number of gates within the quantum circuit. This approach is not scalable and is limited to circuits with up to 10 qubits. Consider choosing an alternative ancilla mode for larger-scale quantum computations.



Total states superposed service
-------------------------------

This service calculates the total number of superposed states in the circuit based on the provided parameters.

**Required parameters:**

- Metric information:

	- `metric` (str): The metric to be used in the quantum computation.
	
- Reference state information:

		- `n_qubits` (int): Number of qubits in the quantum circuit. 
		- `state` (int): Integer representation of the reference quantum state. 
	
	Or
	
		- `state_bin` (str): Binary representation of the reference quantum state.
	
- Distance information:

		- `distances` (list): List of strings distances for specific distances.
	
	Or
	
		- `min_range` (str): Minimum range for distance calculations (included).
		- `max_range` (str): Maximum range for distance calculations (included).
		
	And
	
		- `with_nan` (bool): Specify whether NaN (0/0) values are inclided in the superposition.
		
		
**Example Usage:**

.. code-block:: python

	from qsimov_cloud_client import QsimovCloudClient

	# Initialize QsimovCloudClient with your access token
	client = QsimovCloudClient("your_access_token")

	# Set parameters for the service
	client.set_metric("cosine")
	client.set_state(num_qubits=5, state=2)
	client.set_range(["1/10", "9/10"])
	client.can_have_nan(True)
	client.set_ancilla_mode("clean")

	# Calculate the number of extra superposed states
	n_total_superposed_states = client.calculate_num_superposed()

	# Access the result
	print("The number of superposed states is:", n_total_superposed_states)

.. note::

   Make sure to replace "your_access_token" with your actual Qsimov access token.
	
	