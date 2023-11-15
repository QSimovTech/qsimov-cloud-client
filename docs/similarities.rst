Similarities
============

In this section, we explore various binary similarity measures that are widely used in classical computing. To refresh the nomenclature used:

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

Ample similarity
----------------

Ample similarity can be defined as follows:

.. math::

    s_{Ample}\left(x,y\right)=\left|\frac{a(c+d)}{c(a+b)}\right|
	
- This metric can have **NaN** values :math:`\left(\frac{0}{0}\right)`.

To use the **Ample** similarity metric to generate a quantum superposition, ensure to set the `metric` parameter to **'ample'**.

**Example:** Generation of an Ample quantum superposition.

.. code-block:: python

	from qsimov_cloud_client import QsimovCloudClient

	# Initialize QsimovCloudClient with your access token
	client = QsimovCloudClient("your_access_token")

	# Set parameters for the service
	client.set_metric("ample")
	client.set_state(state_bin='0111010')
	client.set_range(["9/4", "inf"])
	client.can_have_nan(False)
	client.set_ancilla_mode("clean")

	# Generate a quantum circuit
	circuit_superposition = client.generate_circuit()

	# Access the result
	print("The resulting circuit in qasm is:", circuit_superposition.get_qasm_code())

.. note::

   Make sure to replace "your_access_token" with your actual Qsimov access token.

The presented code facilitates the creation of a quantum superposition within the states that have a distance greater than or equal to :math:`\frac{9}{4}=2.25` and less than or equal to :math:`+\infty` from the reference state :math:`0111010\ (58)`. If we simulate the generated QASM code and plot the probabilities of the register where the superposition occurs, obtained from the state vector, we will obtain the following result.

.. image:: /_static/ample_plot.svg

.. note::

	The reference state is highlighted in nova mint color.
	
Cosine similarity
-----------------

Cosine similarity can be defined as follows:

.. math::

    s_{Cosine}\left(x,y\right)=\frac{a}{(a+b)(a+c)}
	
- This metric can have **NaN** values :math:`\left(\frac{0}{0}\right)`.

To use the **Cosine** similarity metric to generate a quantum superposition, ensure to set the `metric` parameter to **'cosine'**.

**Example:** Generation of an **Cosine** quantum superposition.

.. code-block:: python

	from qsimov_cloud_client import QsimovCloudClient

	# Initialize QsimovCloudClient with your access token
	client = QsimovCloudClient("your_access_token")

	# Set parameters for the service
	client.set_metric("cosine")
	client.set_state(state_bin='0111010')
	client.set_range(["1/7", "1/4"])
	client.can_have_nan(False)
	client.set_ancilla_mode("clean")

	# Generate a quantum circuit
	circuit_superposition = client.generate_circuit()

	# Access the result
	print("The resulting circuit in qasm is:", circuit_superposition.get_qasm_code())

.. note::

   Make sure to replace "your_access_token" with your actual Qsimov access token.

The presented code facilitates the creation of a quantum superposition within the states that have a distance greater than or equal to :math:`\frac{1}{7}\approx 0.14286` and less than or equal to :math:`\frac{1}{4}=0.25` from the reference state :math:`0111010\ (58)`. If we simulate the generated QASM code and plot the probabilities of the register where the superposition occurs, obtained from the state vector, we will obtain the following result.

.. image:: /_static/cosine_plot.svg

.. note::

	The reference state is highlighted in nova mint color.

Simpson similarity
------------------

Simpson similarity can be defined as follows:

.. math::

    s_{Simpson}\left(x,y\right)=\frac{a}{min\left(a+b,a+c\right)}
	
- This metric can have **NaN** values :math:`\left(\frac{0}{0}\right)`.

To use the **Simpson** similarity metric to generate a quantum superposition, ensure to set the `metric` parameter to **'simpson'**.

**Example:** Generation of an **Simpson** quantum superposition.

.. code-block:: python

	from qsimov_cloud_client import QsimovCloudClient

	# Initialize QsimovCloudClient with your access token
	client = QsimovCloudClient("your_access_token")

	# Set parameters for the service
	client.set_metric("simpson")
	client.set_state(state_bin='0111010')
	client.set_range(["2/3", "1"])
	client.can_have_nan(False)
	client.set_ancilla_mode("clean")

	# Generate a quantum circuit
	circuit_superposition = client.generate_circuit()

	# Access the result
	print("The resulting circuit in qasm is:", circuit_superposition.get_qasm_code())

The presented code facilitates the creation of a quantum superposition within the states that have a distance greater than or equal to :math:`\frac{2}{3}\approx 0.66667` and less than or equal to :math:`1` from the reference state :math:`0111010\ (58)`. If we simulate the generated QASM code and plot the probabilities of the register where the superposition occurs, obtained from the state vector, we will obtain the following result. 

.. image:: /_static/simpson_plot.svg

.. note::

	The reference state is highlighted in nova mint color.


Johnson similarity
------------------

Johnson similarity can be defined as follows:

.. math::

    s_{Johnson}\left(x,y\right)=\frac{a\left(2a+b+c\right)}{(a+b)(a+c)}
	
- This metric can have **NaN** values :math:`\left(\frac{0}{0}\right)`.

To use the **Johnson** similarity metric to generate a quantum superposition, ensure to set the `metric` parameter to **'johnson'**.

**Example:** Generation of an **Johnson** quantum superposition.

.. code-block:: python

	from qsimov_cloud_client import QsimovCloudClient

	# Initialize QsimovCloudClient with your access token
	client = QsimovCloudClient("your_access_token")

	# Set parameters for the service
	client.set_metric("johnson")
	client.set_state(state_bin='0111010')
	client.set_range(["27/20", "2"])
	client.can_have_nan(False)
	client.set_ancilla_mode("clean")

	# Generate a quantum circuit
	circuit_superposition = client.generate_circuit()

	# Access the result
	print("The resulting circuit in qasm is:", circuit_superposition.get_qasm_code())

The presented code facilitates the creation of a quantum superposition within the states that have a distance greater than or equal to :math:`\frac{27}{20}=1.35` and less than or equal to :math:`2` from the reference state :math:`0111010\ (58)`. If we simulate the generated QASM code and plot the probabilities of the register where the superposition occurs, obtained from the state vector, we will obtain the following result.

.. image:: /_static/johnson_plot.svg

.. note::

	The reference state is highlighted in nova mint color.

Pearson I similarity
--------------------

Pearson I similarity can be defined as follows:

.. math::

    s_{Pearson\ I}\left(x,y\right)=\frac{n\cdot (ad+bc)^{2}}{(a+b)(a+c)(c+d)(b+d)}

- This metric can have **NaN** values :math:`\left(\frac{0}{0}\right)`.

To use the **Pearson I** similarity metric to generate a quantum superposition, ensure to set the `metric` parameter to **'pearson_i'**.

**Example:** Generation of an **Pearson I** quantum superposition.

.. code-block:: python

	from qsimov_cloud_client import QsimovCloudClient

	# Initialize QsimovCloudClient with your access token
	client = QsimovCloudClient("your_access_token")

	# Set parameters for the service
	client.set_metric("pearson_i")
	client.set_state(state_bin='0111010')
	client.set_range(["21/10", "7"])
	client.can_have_nan(False)
	client.set_ancilla_mode("clean")

	# Generate a quantum circuit
	circuit_superposition = client.generate_circuit()

	# Access the result
	print("The resulting circuit in qasm is:", circuit_superposition.get_qasm_code())

The presented code facilitates the creation of a quantum superposition within the states that have a distance greater than or equal to :math:`\frac{21}{10}=2.1` and less than or equal to :math:`7` from the reference state :math:`0111010\ (58)`. If we simulate the generated QASM code and plot the probabilities of the register where the superposition occurs, obtained from the state vector, we will obtain the following result.

.. image:: /_static/pearson_i_plot.svg

.. note::

	The reference state is highlighted in nova mint color.

.. _Jaccard:

Jaccard similarity
------------------

Jaccard similarity can be defined as follows:

.. math::

    s_{Jaccard}\left(x,y\right)=\frac{a}{a+b+c}
	
- This metric can have **NaN** values :math:`\left(\frac{0}{0}\right)`.

To use the **Jaccard** similarity metric to generate a quantum superposition, ensure to set the `metric` parameter to **'jaccard'**.

**Example:** Generation of an **Jaccard** quantum superposition.

.. code-block:: python

	from qsimov_cloud_client import QsimovCloudClient

	# Initialize QsimovCloudClient with your access token
	client = QsimovCloudClient("your_access_token")

	# Set parameters for the service
	client.set_metric("jaccard")
	client.set_state(state_bin='0111010')
	client.set_range(["1/2", "1"])
	client.can_have_nan(False)
	client.set_ancilla_mode("clean")

	# Generate a quantum circuit
	circuit_superposition = client.generate_circuit()

	# Access the result
	print("The resulting circuit in qasm is:", circuit_superposition.get_qasm_code())

The presented code facilitates the creation of a quantum superposition within the states that have a distance greater than or equal to :math:`\frac{1}{2}=0.5` and less than or equal to :math:`1` from the reference state :math:`0111010\ (58)`. If we simulate the generated QASM code and plot the probabilities of the register where the superposition occurs, obtained from the state vector, we will obtain the following result.

.. image:: /_static/jaccard_plot.svg

.. note::

	The reference state is highlighted in nova mint color.

Dice similarity
---------------

Dice similarity can be defined as follows:

.. math::

    s_{Dice}\left(x,y\right)=\frac{2a}{2a+b+c}

- This metric can have **NaN** values :math:`\left(\frac{0}{0}\right)`.

To use the **Dice** similarity metric to generate a quantum superposition, ensure to set the `metric` parameter to **'dice'**.

**Example:** Generation of an **Dice** quantum superposition.

.. code-block:: python

	from qsimov_cloud_client import QsimovCloudClient

	# Initialize QsimovCloudClient with your access token
	client = QsimovCloudClient("your_access_token")

	# Set parameters for the service
	client.set_metric("dice")
	client.set_state(state_bin='0111010')
	client.set_range(["4/7", "1"])
	client.can_have_nan(False)
	client.set_ancilla_mode("clean")

	# Generate a quantum circuit
	circuit_superposition = client.generate_circuit()

	# Access the result
	print("The resulting circuit in qasm is:", circuit_superposition.get_qasm_code())

The presented code facilitates the creation of a quantum superposition within the states that have a distance greater than or equal to :math:`\frac{4}{7}\approx 0.57143` and less than or equal to :math:`1` from the reference state :math:`0111010\ (58)`. If we simulate the generated QASM code and plot the probabilities of the register where the superposition occurs, obtained from the state vector, we will obtain the following result.

.. image:: /_static/dice_plot.svg

.. note::

	The reference state is highlighted in nova mint color.
	
Tanimoto similarity
-------------------

For binary states is same as `Jaccard`_.

	
	
	
	
	
	
