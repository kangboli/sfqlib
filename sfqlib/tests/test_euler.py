from sfqlib.euler_angle import decompose_euler, compose_euler
from numpy import pi
import unittest


class TestDecomposeAfterCompose(unittest.TestCase):
    def test_small_rotation(self):
        """Simple test of functionality with small rotation"""
        rotation = compose_euler(pi/10, pi/10, pi/10)
        alpha, beta, gamma = decompose_euler(rotation)
        self.assertAlmostEqual(alpha, pi/10)
        self.assertAlmostEqual(beta, pi/10)
        self.assertAlmostEqual(gamma, pi/10)

    def test_large_rotation(self):
        """Simple test of functionality with large rotation"""
        rotation = compose_euler(9*pi/10, 9*pi/10, 9*pi/10)
        alpha, beta, gamma = decompose_euler(rotation)
        self.assertAlmostEqual(alpha, 9*pi/10)
        self.assertAlmostEqual(beta, 9*pi/10)
        self.assertAlmostEqual(gamma, 9*pi/10)

    def test_very_small_rotation(self):
        """Test that the decomposition is stable at very small rotation"""
        rotation = compose_euler(pi/10000, pi/10000, pi/10000)
        alpha, beta, gamma = decompose_euler(rotation)
        self.assertAlmostEqual(alpha, pi/10000)
        self.assertAlmostEqual(beta, pi/10000)
        self.assertAlmostEqual(gamma, pi/10000)

    def test_close_to_pi_rotation(self):
        """Test that the decomposition is stable
        for a rotation that is close to pi"""
        rotation = compose_euler(9999*pi/10000, 9999*pi/10000, 9999*pi/10000)
        alpha, beta, gamma = decompose_euler(rotation)
        self.assertAlmostEqual(alpha, 9999*pi/10000)
        self.assertAlmostEqual(beta, 9999*pi/10000)
        self.assertAlmostEqual(gamma, 9999*pi/10000)

    def test_free_precession(self):
        """Test the cases of singularity"""
        rotation = compose_euler(0, 0, 9*pi/10)
        alpha, beta, gamma = decompose_euler(rotation)
        self.assertAlmostEqual(alpha, 0)
        self.assertAlmostEqual(beta, 0)
        self.assertAlmostEqual(gamma, 9*pi/10)

    def test_pi_rotation(self):
        """Test the cases of singularity"""
        rotation = compose_euler(0, pi, 9*pi/10)
        alpha, beta, gamma = decompose_euler(rotation)
        self.assertAlmostEqual(alpha, 0)
        self.assertAlmostEqual(beta, pi)
        self.assertAlmostEqual(gamma, 9*pi/10)


if __name__ == '__main__':
    unittest.main()
