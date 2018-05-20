Fancy Qubits.
=============

The basic qubit runs at the speed of C++ when numpy uses MKL.
To maintain that speed, operations that harm performance are separated into FancyQubits.
Currently, there are two main features in FancyQubits.

#. Euler angle.
#. Qubit Visualization.

=============
SfqFancyQubit
=============

.. autoclass:: sfqQubit.SfqFancyQubit
   :members:
   :inherited-members:

   .. automethod:: __init__

   .. attribute:: alpha_list

      List of :math:`\alpha` Euler angle

   .. attribute:: beta_list

      List of :math:`\beta` Euler angle

   .. attribute:: gamma_list

      List of :math:`\gamma` Euler angle

===================
Sfq2LevelFancyQubit
===================

.. autoclass:: sfqQubit.Sfq2LevelFancyQubit
   :members:
   :inherited-members:

   .. automethod:: __init__

===================
Sfq3LevelFancyQubit
===================

.. autoclass:: sfqQubit.Sfq3LevelFancyQubit
   :members:
   :inherited-members:

   .. automethod:: __init__
