"""Setup configuration for the dataudit package."""

from setuptools import find_packages, setup


setup(
    name="dataudit",
    version="0.1.0",
    description="Professional dataset profiling with multi-sheet Excel reports.",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.23,<2",
        "pandas>=1.5",
        "openpyxl>=3.1",
    ],
    python_requires=">=3.8",
)
