"""Test that the code reproduces the old results
of earlier versions of the code."""
from sfqlib._sfqQubitLegacy import Sfq3LevelQubit as Sfq3Legacy,\
    Sfq2LevelQubit as Sfq2Legacy
from sfqlib.sfqQubit import Sfq3LevelQubit, Sfq2LevelQubit
from numpy import pi, linspace
import unittest


"""Helper method for testing"""
def test_sweep_d_theta(Qubit):
    """Resonance sequence. Sweep d_theta"""
    n = linspace(10, 500, 10)
    fidelities = list()
    for num_steps in n:
        qubit = Qubit((pi/2.0/num_steps))
        qubit.resonance()
        fidelities.append(qubit.measure_fidelity())
    return [1.0-f for f in fidelities]


def test_sweep_d_theta_with_pattern(Qubit):
    """Resonance sequence. Sweep d_theta,
    using explicitly constructed pulse sequence"""
    n = linspace(10, 500, 10)
    fidelities = list()
    for j, num_steps in enumerate(n):
        pattern = make_resonance_pattern(num_steps)
        qubit = Qubit((pi/2.0/num_steps))
        qubit.pulse_pattern(pattern)
        fidelities.append(qubit.measure_fidelity())
    return [1.0-f for f in fidelities]


def test_sweep_qubit_frequency(Qubit, d_theta, marker='b'):
    """Resonance sequence using Qubits with frequency
    not commensurate with that of the clock."""
    fidelities = list()
    w_qubit_space = linspace(2*pi*4.99e9, 2*pi*5.01e9, 10)
    for w01 in w_qubit_space:
        qubit = Qubit(d_theta=d_theta, w_qubit=(w01, 2*w01-2*pi*0.2e9))
        qubit.resonance()
        fidelities.append(qubit.measure_fidelity())
    return [1.0-f for f in fidelities]


def make_resonance_pattern(num):
    """
    Create a pulse pattern of [1, 1, 1, ...].
    Only for the case when the clock frequency is the qubit frequency.
    """
    return [1 for i in range(int(num))]


class TestFidelityMeasurement(unittest.TestCase):
    def test_measure_fidelity_with_no_rotation(self):
        """The fidelity should be 1 when no rotation is applied."""
        qubit = Sfq3LevelQubit(d_theta=pi/200, w_clock=2*pi*40e9,
                 w_qubit=(2*pi*5.0e9, 2*pi*10.0e9), theta=0)
        gate_fidelity = qubit.measure_fidelity(method='gates')
        state_fidelity = qubit.measure_fidelity(method='states')
        self.assertAlmostEqual(gate_fidelity, 1.0)
        self.assertAlmostEqual(state_fidelity, 1.0)

    def test_measure_fidelity_with_long_resonant_sequence(self):
        """The fidelity should be close to one for a very long resonant sequence."""
        qubit = Sfq3LevelQubit(d_theta=pi/2000, w_clock=2*pi*40e9,
                               w_qubit=(2*pi*5.0e9, 2*pi*10.0e9), theta=0)
        qubit.resonance()
        gate_fidelity = qubit.measure_fidelity(method='gates')
        state_fidelity = qubit.measure_fidelity(method='states')
        self.assertAlmostEqual(gate_fidelity, 1.0, 5)
        self.assertAlmostEqual(state_fidelity, 1.0, 5)


class TestReproduceOldResults(unittest.TestCase):
    """Test that new version of the code reproduce the old results."""
    def test_resonance_sequence_3_level(self):
        legacy_resonance = test_sweep_d_theta(Sfq3Legacy)
        dev_resonance = test_sweep_d_theta(Sfq3LevelQubit)
        self.assert_sequence_equal(legacy_resonance, dev_resonance)

    def test_resonance_sequence_with_pattern_3_level(self):
        legacy_resonance_with_pattern = test_sweep_d_theta_with_pattern(
            Sfq3Legacy)
        dev_resonance_with_pattern = test_sweep_d_theta_with_pattern(
            Sfq3LevelQubit)
        self.assert_sequence_equal(legacy_resonance_with_pattern,
                                   dev_resonance_with_pattern)

    def test_drift_3_level(self):
        legacy_drift = test_sweep_qubit_frequency(Sfq3Legacy, pi/2.0/50)
        dev_drift = test_sweep_qubit_frequency(Sfq3LevelQubit, pi/2.0/50)
        self.assert_sequence_equal(legacy_drift, dev_drift)

    def test_resonance_sequence_2_level(self):
        legacy_resonance = test_sweep_d_theta(Sfq2Legacy)
        dev_resonance = test_sweep_d_theta(Sfq2LevelQubit)
        self.assert_sequence_equal(legacy_resonance, dev_resonance)

    def test_resonance_sequence_with_pattern_2_level(self):
        legacy_resonance_with_pattern = test_sweep_d_theta_with_pattern(
            Sfq2Legacy)
        dev_resonance_with_pattern = test_sweep_d_theta_with_pattern(
            Sfq2LevelQubit)
        self.assert_sequence_equal(legacy_resonance_with_pattern,
                                   dev_resonance_with_pattern)

    def test_drift_2_level(self):
        legacy_drift = test_sweep_qubit_frequency(Sfq2Legacy, pi/2.0/50)
        dev_drift = test_sweep_qubit_frequency(Sfq2LevelQubit, pi/2.0/50)
        self.assert_sequence_equal(legacy_drift, dev_drift)

    def assert_sequence_equal(self, seq1, seq2):
        self.assertEqual(len(seq1), len(seq2))
        for l, d in zip(seq1, seq2):
            self.assertAlmostEqual(l, d, 5)


if __name__ == '__main__':
    unittest.main()

# fig, (ax0, ax1, ax2) = plt.subplots(3, 1)
# ax0.plot(legacy_resonance)
# ax1.plot(legacy_resonance_with_pattern)
# ax2.plot(legacy_drift)
# plt.show()
