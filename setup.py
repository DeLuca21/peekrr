from setuptools import setup, find_packages

setup(
    name='peekrr',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "questionary",
        "requests",
        "rich",
        "PyYAML",
        "rapidfuzz",
    ],
    entry_points={
        'console_scripts': [
            'peekrr = peekrr.main:main'
        ]
    },
    author='Your Name',
    description='CLI tool for interacting with Jellyseerr',
    url='https://github.com/DeLuca21/peekrr',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.7',
)
