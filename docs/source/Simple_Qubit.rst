Simple Qubit.
=============

When a qubit is created, it starts at :math:`|0>` state.
However, all 6 cardinal states on the block sphere are tracked.

========
SfqQubit
========

.. autoclass:: sfqQubit.SfqQubit
   :members:

   .. automethod:: __init__

==============
Sfq3LevelQubit
==============

.. autoclass:: sfqQubit.Sfq3LevelQubit
   :members:
   :inherited-members:
   :exclude-members: measure_fidelity

   .. automethod:: measure_fidelity

      If 'states' is provided,

      .. math::

         F_{avg} = \frac{1}{6} \sum_{\alpha} Tr\{U_G\rho_{\alpha}U^{\dagger}_G U_{id}\rho_{\alpha}U_{id}^{\dagger}\}

      Where :math:`\alpha = \pm x, \pm y, \pm z`.

      If 'gates' is provided,

      .. math::

         F_{avg} = \frac{1}{6} \left( Tr\{U^{\dagger}_G \mathcal{P} U_G \mathcal{P} \} + | Tr\{\mathcal{P} U_{id}^{\dagger} U_G\}|^2 \right)


      Where :math:`U_{id}` is the ideal gate, and :math: `\mathcal{P}` is
      the projection onto qubit subspace.


==============
Sfq2LevelQubit
==============

.. autoclass:: sfqQubit.Sfq2LevelQubit
      :members:
      :inherited-members:
      :exclude-members: measure_fidelity

      .. automethod:: measure_fidelity

         If 'states' is provided,

         .. math::

            F_{avg} = \frac{1}{6} \sum_{\alpha} Tr\{U_G\rho_{\alpha}U^{\dagger}_G U_{id}\rho_{\alpha}U_{id}^{\dagger}\}

         Where :math:`\alpha = \pm x, \pm y, \pm z`.

===========
SfqSequence
===========

.. autoclass:: sfqQubit.SfqSequence
    :members:

    .. automethod:: __init__