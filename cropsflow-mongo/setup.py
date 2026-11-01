# setup.py
from setuptools import setup, find_packages

setup(
    name="cropsflow-mongo",
    version="0.1.0",
    description="Mongo data base module for cropsFlow",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Med Mahdi Maarouf",
    author_email="info@cropsflow.com",
    url="https://github.com/cropsflow/cropsflow-mongo",  # Your project URL
    packages=find_packages(include=["cropsflow_mongo", "cropsflow_mongo.*"]),
    install_requires=[
        "pymongo~=4.10.1"
    ],
    dependency_links=[
        "C:/Users/msi/Desktop/CropsFlow/workspace/cropsflow"
    ],
    extras_require={
        "dev": [
            "pytest",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
