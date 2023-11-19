Distances
=========

In this section, we explore various binary distance measures that are widely used in classical computing. To refresh the nomenclature used:

.. list-table:: 
   :widths: 25 25 25
   :header-rows: 1
   :align: center

   * - 
     - **1 (Presence in x)**
     - **0 (Absence in x)**
   * - **1 (Presence in y)**
     - :math:`a = x\cdot y` 
     - :math:`b = \overline{x}\cdot y`  
   * - **0 (Absence in y)**
     - :math:`c = x\cdot \overline{y}` 
     - :math:`d = \overline{x}\cdot \overline{y}` 


Hamming distance
----------------

Hamming distance can be defined as a metric that quantifies the dissimilarity between two binary states of equal length by measuring the number of positions at which the corresponding bits differ. The formula is as follows:


.. math::

    d_{Hamming}\left(x,y\right)=b+c
	
- This metric can **NOT** have **NaN** values :math:`\left(\frac{0}{0}\right)`.
	
To use the Hamming distance metric to generate a quantum superposition, ensure to set the `metric` parameter to **'hamming'**.

**Example:** Generation of a Hamming quantum superposition.

.. code-block:: python

	from qsimov_cloud_client import QsimovCloudClient

	# Initialize QsimovCloudClient with your access token
	client = QsimovCloudClient("your_access_token")

	# Set parameters for the service
	client.set_metric("hamming")
	client.set_state(state_bin='0111010')
	client.set_range(["0", "3"])
	client.can_have_nan(False)
	client.set_ancilla_mode("clean")

	# Generate a quantum circuit
	circuit_superposition = client.generate_circuit()

	# Access the result
	print("The resulting circuit in qasm is:", circuit_superposition.get_qasm_code())

The presented code facilitates the creation of a quantum superposition within the states that have a distance greater than or equal to :math:`0` and less than or equal to :math:`3` from the reference state :math:`0111010\ (58)`. If we simulate the generated QASM code and plot the probabilities of the register where the superposition occurs, obtained from the state vector, we will obtain the following result.

.. image:: /_static/hamming_plot.svg
	
.. note::

	The reference state is highlighted in nova mint color.