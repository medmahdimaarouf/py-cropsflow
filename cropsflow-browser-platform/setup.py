# setup.py
from setuptools import setup, find_packages

setup(
    name="cropsflow-dom",
    version="0.1.0",
    description="CropsFlow for Python",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Med Mahdi Maarouf",
    author_email="info@cropsflow.com",
    url="https://github.com/cropsflow/cropsflow-dom",  # Your project URL
    packages=find_packages(include=["cropsflow_dom", "cropsflow_dom.*"]),
    install_requires=[
        'lxml',
        "cssselect"
    ],
    dependency_links=[
        "C:/Users/msi/Desktop/CropsFlow/workspace/cropsflow",

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
