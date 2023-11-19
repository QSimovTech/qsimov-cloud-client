.. _getting_started:

Getting Started
===============

Installation
------------

To use the QsimovCloudClient in your Python projects, follow these installation steps:

1. **Install QsimovCloudClient:**

   You can install QsimovCloudClient using `pip`:

   .. code-block:: shell

      pip install qsimov-cloud-client

Basic Usage
-----------

Now that you have QsimovCloudClient installed, you can use it in your projects. Here's a simple example:

.. code-block:: python

   	from qsimov_cloud_client import QsimovCloudClient

	# Initialize QsimovCloudClient with your access token
	client = QsimovCloudClient("your_access_token")

	# Set parameters for the service
	client.set_metric("ample")
	client.set_state(state_bin='0111010')
	client.set_distances(["0", "9/4", "inf"])
	client.can_have_nan(False)
	client.set_ancilla_mode("clean")

	# Generate a quantum circuit
	circuit_superposition = client.generate_circuit()

	# Access the result
	print("The resulting circuit in qasm is:", circuit_superposition.get_qasm_code())
	
	# Additional usage examples can be found in the documentation.

.. note::

   Make sure to replace "your_access_token" with your actual Qsimov access token.

For more detailed information and advanced usage, refer to the full documentation.

Important considerations
------------------------

- Circuits **requiring ancilla** qubits will have them in the **most significant** qubits, while the state with superposition will be in the least significant ones.
- Any **distance argument** should be provided as **string**. If they include decimals, use fraction format (e.g., '3/2' for 1.5).
- Using the **"noancilla"** ancilla mode may result in **exponential growth** in the number of gates within the quantum circuit. This approach is not scalable and is limited to circuits with up to 10 qubits. Consider choosing an alternative ancilla mode for larger-scale quantum computations.
- All generated circuits will be decomposed into the **u3**, **cx**, and **cxx** gates.