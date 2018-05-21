from setuptools import setup
setup(
    name='sfqlib',
    packages=['sfqlib'],
    version='0.1.4',
    description='Tools for SFQ research',
    long_description="This package contains tools for simulating qubit control with Single Flux Quantum Pulse(SFQ) Trains. This package is under development. Contributions are welcome.",
    author='Kangbo Li',
    author_email='kli89@wisc.edu',
    package_data={'sfqlib': ['theory/theory.pdf'], },
    url='https://github.com/hannoeichel/sfqlib',
    keywords=['SFQ', 'Control'],
    install_requires=['numpy', 'scipy', ],
    license='MIT',
    classifiers=[],
)
