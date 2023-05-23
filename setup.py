from setuptools import setup, find_packages

setup(
    name='yolo_dummy_data',
    version='0.1.0',
    author='Jerzy Słomkowski',
    description='simple script to generate dummy data for YOLO training',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'matplotlib',
        'git+https://github.com/jslomkowski/yolo_dummy_data.git',

    ],
    entry_points={
        'console_scripts': [
            'generate_shapes_dataset=yolo_dummy_data.generate_shapes_dataset:main',
        ],
    },
)
