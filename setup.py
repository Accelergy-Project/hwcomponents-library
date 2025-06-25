from setuptools import setup, find_packages
import os


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="hwcomponents_library",
    version="0.1",
    description="A library of hardware components for energy estimation.",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: " "Electronic Design Automation (EDA)",
    ],
    keywords="hardware components energy estimation",
    author="Tanner Andrulis",
    author_email="andrulis@Mit.edu",
    license="MIT",
    install_requires=[],
    python_requires=">=3.12",
    packages=find_packages(include=["hwcomponents_library", "hwcomponents_library.*"]),
    include_package_data=True,
)
