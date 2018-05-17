"""Test that the code reproduces the old results
of earlier versions of the code."""
from sfqlib._sfqQubitLegacy import Sfq3LevelQubit as Sfq3Legacy,\
    Sfq2LevelQubit as Sfq2Legacy
from sfqlib.sfqQubit import Sfq3LevelQubit, Sfq2LevelQubit
import numpy as np
import unittest
# import matplotlib.pyplot as plt


def test_sweep_d_theta(Qubit):
    """Resonance sequence. Sweep d_theta"""
    n = np.linspace(10, 500, 10)
    fidelities = list()
    for num_steps in n:
        qubit = Qubit((np.pi/2.0/num_steps))
        qubit.resonance()
        fidelities.append(qubit.measure_fidelity())
    return [1.0-f for f in fidelities]


def test_sweep_d_theta_with_pattern(Qubit):
    """Resonance sequence. Sweep d_theta,
    using explicitly constructed pulse sequence"""
    n = np.linspace(10, 500, 10)
    fidelities = list()
    for j, num_steps in enumerate(n):
        pattern = list()
        pattern = make_resonance_pattern(num_steps)
        qubit = Qubit((np.pi/2.0/num_steps))
        qubit.pulse_pattern_euler(pattern)
        fidelities.append(qubit.measure_fidelity())
    return [1.0-f for f in fidelities]


def test_sweep_qubit_frequency(Qubit, d_theta, marker='b'):
    """Resonance sequence using Qubits with frequency
    not commensurate with that of the clock."""
    fidelities = list()
    w_qubit_space = np.linspace(2*np.pi*4.99e9, 2*np.pi*5.01e9, 10)
    for w01 in w_qubit_space:
        qubit = Qubit(d_theta=d_theta, w_qubit=(w01, 2*w01-2*np.pi*0.2e9))
        qubit.resonance()
        fidelities.append(qubit.measure_fidelity())
    return [1.0-f for f in fidelities]


def make_resonance_pattern(num):
    """
    Create a pulse pattern of [1, 1, 1, ...].
    Only for the case when the clock frequency is the qubit frequency.
    """
    return [1 for i in range(int(num))]


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
        legacy_drift = test_sweep_qubit_frequency(Sfq3Legacy, np.pi/2.0/50)
        dev_drift = test_sweep_qubit_frequency(Sfq3LevelQubit, np.pi/2.0/50)
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
        legacy_drift = test_sweep_qubit_frequency(Sfq2Legacy, np.pi/2.0/50)
        dev_drift = test_sweep_qubit_frequency(Sfq2LevelQubit, np.pi/2.0/50)
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
