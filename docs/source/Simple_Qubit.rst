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
Sfq2LevelQubit
==============

.. autoclass:: sfqQubit.Sfq2LevelQubit

   .. autoattribute:: kets

   .. automethod:: pulse_pattern

   .. automethod:: resonance

   .. automethod:: precess

      Evolve according to the time evolution operator:

      .. math::
         :nowrap:

             \begin{equation}
         U_{free} =
         \begin{bmatrix}
         1 & 0 \\
         0 & e^{-j\omega_{01} \tau}
         \end{bmatrix}
         \end{equation}

    Where :math:`\tau` is one clock period.
 
   .. automethod:: pulse_and_precess
 
      Evolve according to the time evolution operator
 
      .. math::
         :nowrap:
 
             \begin{equation}
         U_{SFQ} =
         \begin{bmatrix}
         cos(d \theta / 2)           &  - sin (d \theta / 2)\\
         sin (d \theta / 2)          &  cos(d \theta / 2)
         \end{bmatrix}
         \end{equation}
 
   .. automethod:: measure_fidelity
 
      If 'states' is provided,
 
      .. math::
 
        F_{avg} = \frac{1}{6} \sum_{\alpha} Tr\{U_G\rho_{\alpha}U^{\dagger}_G U_{id}\rho_{\alpha}U_{id}^{\dagger}\}

     Where :math:`\alpha = \pm x, \pm y, \pm z`.


==============
Sfq3LevelQubit
==============

.. autoclass:: sfqQubit.Sfq3LevelQubit

   .. autoattribute:: kets

   .. automethod:: pulse_pattern

   .. automethod:: resonance

   .. automethod:: precess

      Evolve according the the time evolution operator:

      .. math::
        :nowrap:

        \begin{equation}
        U_{free} =
        \begin{bmatrix}
        1 & 0 & 0 \\
        0 & e^{-j\omega_{01} \tau} & 0 \\
        0 & 0 & e^{-j\omega_{02} \tau}
        \end{bmatrix}
        \end{equation}

      Where :math:`\tau` is one clock period.

   .. automethod:: pulse_and_precess

      Evolve according to the time evolution operator

      .. math::
        :nowrap:

        \begin{equation}
        U_{SFQ} =
        \begin{bmatrix}
        -1\alpha           &  -1 \beta         & -\sqrt{2} \alpha\\
        1 \beta            &  -3\alpha         & -\sqrt{2} \beta\\
        \sqrt{2} \alpha    &    \sqrt{2}\beta  &-2 \alpha
        \end{bmatrix}
        \end{equation}

      Where

      :math:`\alpha  = \left( -\frac{1}{3} cos \left(-\sqrt{3} \frac{\delta \theta}{2} \right) + \frac{1}{3} \right)`,

      :math:`\beta = \left( \frac{1}{\sqrt{3}} sin\left(\sqrt{3} \frac{\delta \theta}{2} \right) \right)`,

   .. automethod:: measure_fidelity

      If 'states' is provided,

      .. math::

         F_{avg} = \frac{1}{6} \sum_{\alpha} Tr\{U_G\rho_{\alpha}U^{\dagger}_G U_{id}\rho_{\alpha}U_{id}^{\dagger}\}

      Where :math:`\alpha = \pm x, \pm y, \pm z`.

      If 'gates' is provided,

      .. math::

         F_{avg} = \frac{1}{6} \left( Tr\{U^{\dagger}_G \mathcal{P} U_G \mathcal{P} \} + | Tr\{\mathcal{P} U_{id}^{\dagger} U_G\}|^2 \right)


      Where :math:`U_{id}` is the ideal gate, and :math:`\mathcal{P}` is
      the projection onto qubit subspace.

===========
SfqSequence
===========

.. autoclass:: sfqQubit.SfqSequence
    :members:

    .. automethod:: __init__
