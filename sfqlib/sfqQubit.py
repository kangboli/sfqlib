"""
Tool for SFQ research.
__author__ = "Kangbo Li"
__copyright__ = "Copyright 2018, The SFQ Project"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Kangbo Li"
__email__ = "kli89@wisc.edu"
__status__ = "Beta"
"""

from scipy.linalg import expm
from numpy import array, complex64, sqrt, pi, \
    absolute, exp, dot, angle, cos, sin, conj
from sfqlib.euler_angle import decompose_euler
from copy import deepcopy

class SfqSequence():
    def __init__(self, sequence_dec, length):
        """
        :param int sequence_dec: The sequence specified as an integer.
        This will be later converted to a binary as a bit string.
        :apram int length: The length of the bit string.
        If the sequence_dec is too large to be represented by a length bits,
        it will be truncated.
        """
        self.decimal = sequence_dec
        self.length = length
        self.fidelity = 0
        self.qubit = None

    @property
    def binary(self):
        """Return the sequence as a bit string."""
        return list(self.decimal_to_binary(self.decimal, self.length))

    def plot_sequence(self, ax):
        for index, bit in enumerate(self.binary):
            if bit == 1:
                ax.plot([index, index], [0, 1], 'b')
            else:
                ax.plot([index, index], [0, 0], 'b')

    @staticmethod
    def decimal_to_binary(num, digits):
        """Convert a number from decimal to binary (in reversed order).
        e.g. 6 -> [0, 1, 1]"""
        for i in range(digits):
            yield num % 2
            num = num / 2


class SfqQubit(object):
    g, e, p, p_i, m, m_i = None, None, None, None ,None, None
    s_kets = [g, e, m, m_i, p, p_i]
    a, a_dag = None, None
    """Qubit controlled by SFQ pulses. This class is to be subclassed."""
    def __init__(self, d_theta=pi/200, w_clock=2*pi*5e9,
                 w_qubit=(2*pi*5.0e9, 2*pi*9.8e9), theta=pi/2):
        """
        Create a qubit controlled by SFQ pulses.
        :param float d_theta: Angle of single y-rotation.
        :param float w_clock: Clock frequency
        :param (float, float) w_qubit: (Qubit frequency,
        Leakage level frequency)
        :param float theta: Total rotation.
        """
        self.usfq, self.ufr = None, None
        self.w10, self.w12 = w_qubit
        self.w_clock = w_clock
        self.d_theta, self.theta = d_theta, theta
        self.d_phi = self.w10 / self.w_clock * 2 * pi
        self.d_phi3 = (self.w10 + self.w12) / self.w10 * self.d_phi
        self.resonance_times = int(round(self.w_clock/self.w10, 0))
        self.r_kets = [self._ideal_rotation(ket) for ket in self.s_kets]

    @property
    def kets(self):
        return [dot(self.u, ket) for ket in self.s_kets]

    def precess(self):
        """Precess the qubit for one clock period."""
        self.u = dot(self.u, self.ufr)

    def _pulse(self):
        self.u = dot(self.u, self.usfq)

    def pulse_and_precess(self):
        """Rotate the qubit for d_theta around y-axes,
        followed by precession for one clock period."""
        self._pulse()
        self.precess()

    def measure_fidelity(self):
        """Measure the fidelity. Implement in subclasses."""
        pass

    def resonance(self):
        """Resonance pulse sequence. The pulses are spaced by d_phi
        TODO TEST RESONANCE"""
        num_steps = self.theta / self.d_theta
        for step in range(int(num_steps)):
            self.pulse_and_precess()
            for i in range(self.resonance_times-1):
                self.precess()

    def pulse_pattern(self, pattern):
        """
        Evolve the qubit according to a sequence of
        0 (precession) and 1 (sfq pulse_and_precess).
        :param list[int] pattern: The pulse sequence.
        """
        while pattern:
            if pattern.pop() == 1:
                self.pulse_and_precess()
            else:
                self.precess()

    def _ideal_rotation(self, ket):
        """
        Rotate the pauli states according to the ideal y-rotation.
        Implement in subclasses.
        :return: The rotated state
        """
        pass


class Sfq3LevelQubit(SfqQubit):
    """Qubit with leakage level."""
    g = array([1.0, 0.0, 0.0], dtype=complex64)
    e = array([0.0, 1.0, 0.0], dtype=complex64)
    p = 1.0/sqrt(2.0)*array([1.0, 1.0, 0.0], dtype=complex64)
    p_i = 1.0/sqrt(2.0)*array([1.0, 1.0j, 0.0], dtype=complex64)
    m = 1.0/sqrt(2.0)*array([1.0, -1.0, 0.0], dtype=complex64)
    m_i = 1.0/sqrt(2.0)*array([1.0, -1.0j, 0.0], dtype=complex64)
    s_kets = [g, e, m, m_i, p, p_i]
    a = array([[0.0, 1.0, 0.0], [0.0, 0.0, sqrt(2.0)],
               [0.0, 0.0, 0.0]], dtype=complex64)
    a_dag = array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0],
                   [0.0, sqrt(2.0), 0.0]], dtype=complex64)
    def __init__(self, d_theta=pi/200, w_clock=2*pi*5e9,
                 w_qubit=(2*pi*5.0e9, 2*pi*9.8e9), theta=pi/2):
        super(Sfq3LevelQubit, self).__init__(d_theta, w_clock, w_qubit, theta)
        """Initialize all the kets and operators for the three level qubit."""
        self.ufr = array([[1.0, 0.0, 0.0],
                          [0.0, exp(-1.0j * self.d_phi), 0.0],
                          [0.0, 0.0, exp(-1.0j * self.d_phi3)]],
                         dtype=complex64)
        self.usfq = expm(array(self.d_theta/2.0*(self.a_dag-self.a),
                               dtype=complex64))
        self.u = array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=complex64)

    def measure_fidelity(self, ignore_leakage=False):
        kets, r_kets = self.kets, self.r_kets
        if ignore_leakage:
            kets = [[ket[0], ket[1], 0] for ket in kets]
            r_kets = [[r_ket[0], r_ket[1], 0] for r_ket in r_kets]
        fidelity = [pow(absolute(dot(conj(r_ket), ket)), 2)
                    for r_ket, ket in zip(r_kets, kets)]
        return sum(fidelity)/len(fidelity)

    def _ideal_rotation(self, ket):
        ideal_gate = array([[cos(self.theta/2), sin(self.theta/2), 0],
                            [-sin(self.theta/2), cos(self.theta/2), 0],
                            [0, 0, 1]], dtype=complex64)
        return dot(ideal_gate, ket)


class Sfq2LevelQubit(SfqQubit):
    g = array([1.0, 0.0], dtype=complex64)
    e = array([0.0, 1.0], dtype=complex64)
    p = 1.0/sqrt(2.0)*array([1.0, 1.0], dtype=complex64)
    p_i = 1.0/sqrt(2.0)*array([1.0, 1.0j], dtype=complex64)
    m = 1.0/sqrt(2.0)*array([1.0, -1.0], dtype=complex64)
    m_i = 1.0/sqrt(2.0)*array([1.0, -1.0j], dtype=complex64)
    s_kets = [g, e, m, m_i, p, p_i]
    a = array([[0.0, 1.0], [0.0, 0.0]], dtype=complex64)
    a_dag = array([[0.0, 0.0], [1.0, 0.0]], dtype=complex64)
    def __init__(self, d_theta=pi/200, w_clock=2*pi*5e9,
                 w_qubit=(2*pi*5.0e9, 2*pi*9.8e9), theta=pi/2):
        # The leakage frequency is specified even though
        # leakage level is not present. This is a design error.
        super(Sfq2LevelQubit, self).__init__(d_theta, w_clock, w_qubit, theta)
        """Initialize all the kets and operators for the two level qubit."""
        self.ufr = array([[1.0, 0.0],
                          [0.0, exp(-1.0j * self.d_phi)]],
                         dtype=complex64)
        self.usfq = expm(array(self.d_theta/2.0*(self.a_dag-self.a), dtype=complex64))
        self.u = array([[1, 0], [0, 1]], dtype=complex64)

    def measure_fidelity(self):
        kets, r_kets = self.kets, self.r_kets
        fidelity = [pow(absolute(dot(conj(r_ket), ket)), 2)
                    for r_ket, ket in zip(r_kets, kets)]
        return sum(fidelity)/len(fidelity)

    def _ideal_rotation(self, ket):
        ideal_gate = array([[cos(self.theta/2), sin(self.theta/2)],
                            [-sin(self.theta/2), cos(self.theta/2)]],
                           dtype=complex64)
        return dot(ideal_gate, ket)


"""
Euler qubits tracks the euler angles of the rotation
in addition to the state kets.
They are separated from the normal qubits to improve performance
"""

class SfqFancyQubit(SfqQubit):
    def __init__(self, d_theta=pi/200, w_clock=2*pi*5e9,
                 w_qubit=(2*pi*5.0e9, 2*pi*9.8e9), theta=pi/2):
        super(SfqQubit, self).__init__(d_theta, w_clock,
                                                  w_qubit, theta)

    def _init_euler_angles(self):
        self.alpha_list, self.beta_list, self.gamma_list = list(), list() ,list()

    def pulse_pattern_euler(self, pattern):
        while pattern:
            if pattern.pop() == 1:
                self.pulse_and_precess()
            else:
                self.precess()
            # Keep track of the euler angles.
            alpha, beta, gamma = decompose_euler(self.u)
            self.alpha_list.append(alpha)
            self.beta_list.append(beta)
            self.gamma_list.append(gamma)


class Sfq2LevelFancyQubit(Sfq2LevelQubit, SfqFancyQubit):
    def __init__(self, d_theta=pi/200, w_clock=2*pi*5e9,
                 w_qubit=(2*pi*5.0e9, 2*pi*9.8e9), theta=pi/2):
        super(Sfq2LevelFancyQubit, self).__init__(d_theta, w_clock,
                                                  w_qubit, theta)
        self._init_euler_angles()

        """In addition to the 6 cardinal states,
        we record the euler angles."""


class Sfq3LevelFancyQubit(Sfq3LevelQubit, SfqFancyQubit):
    def __init__(self, d_theta=pi/200, w_clock=2*pi*5e9,
                 w_qubit=(2*pi*5.0e9, 2*pi*9.8e9), theta=pi/2):
        super(Sfq3LevelFancyQubit, self).__init__(d_theta, w_clock,
                                                  w_qubit, theta)
        self._init_euler_angles()
