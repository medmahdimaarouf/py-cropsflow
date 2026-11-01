# setup.py
from setuptools import setup, find_packages

setup(
    name="cropsflow-http",
    version="0.1.0",
    description="Http module for CropsFlow framework",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Med Mahdi Maarouf",
    author_email="info@cropsflow.com",
    url="https://github.com/cropsflow/cropsflow-http",  # Your project URL
    packages=find_packages(include=["cropsflow_http", "cropsflow_http.*"]),
    install_requires=['lxml', 'requests'],
    extras_require={
        "dev": [
            "pytest",
            "pytest-asyncio"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
