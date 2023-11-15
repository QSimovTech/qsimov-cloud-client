Metrics
=======

The quantum superposition neighborhood can be generated according to different criteria. Here, we have the two main groups of available metrics:

- **Distance** is a quantitative measure representing the magnitude of the difference between two states. The **greater the distance**, the **higher the dissimilarity** between the states.

- **Similarity** is a measure that quantifies the degree of likeness or relationship between two states. The **greater the similarity**, the **closer or more concordant the states are**.

The following nomenclature will be followed when referring to binary strings:

- Binary strings will be represented as **x** and **y**, each consisting of binary digits (0s and 1s).
- :math:`a`: Number of bits where both **x** and **y** have the value 1 (presence), indicating **positive matches**.
- :math:`b`: Number of bits where the value of **x** is 0 and **y** is 1, indicating **x absence mismatches**.
- :math:`c`: Number of bits where the value of **x** is 1 and **y** is 0, indicating **y absence mismatches**.
- :math:`d`: Number of bits where both **x** and **y** have the value 0 (absence), indicating **negative matches**.

The binary metrics discussed here offer insights into the dissimilarity or similarity between binary strings. The formulas for these distances are presented with respect to the mentioned nomenclature.

Additional considerations:

- The diagonal sum :math:`a+d` represents the total number of matches between **x** and **y**.
- The other diagonal sum :math:`b+c` represents the total number of mismatches between **x** and **y**.
- The total sum of :math:`a+b+c+d`, is always equal to :math:`n` (the total number of bits).

Below is a table summarizing the nomenclature used:

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


These conventions are adapted from the guidelines presented in the article :cite:`Choi2009`.

.. toctree::
   :maxdepth: 4

   distances
   similarities
   
   
