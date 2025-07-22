from setuptools import setup, find_packages

setup(
    name='SudokuGenerator',
    version='1.0.0',
    description='A printable sudoku puzzle generator',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'fpdf',
    ],
    entry_points={
        'console_scripts': [
            'sudoku-generator = cli:main',
        ],
    },
) 