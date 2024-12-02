# setup.py

from setuptools import setup, find_packages

setup(
    name='pyproxtractor-core',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    author='Pro Extractor',
    author_email='info@proxtractor.com',
    description='Python core librtary for Pro Extractor',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/proxtractor/pyproxtractor-core',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
