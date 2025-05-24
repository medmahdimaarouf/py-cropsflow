# setup.py
from setuptools import setup, find_packages

setup(
    name="cropsflow",
    version="0.1.0",
    description="CropsFlow for Python",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Med Mahdi Maarouf",
    author_email="info@cropsflow.com",
    url="https://github.com/cropsflow/cropsflow",  # Your project URL
    packages=find_packages(include=["cropsflow", "cropsflow.*"]),
    install_requires=[
        'lxml',
        'fastapi'
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
