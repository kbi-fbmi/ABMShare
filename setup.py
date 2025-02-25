from setuptools import find_packages, setup

"""
ABMSHARE installation. Requirements are listed in requirements.txt. There are two
options:
    pip install .       # Standard install
    pip install . -e      # Install in editable mode
Make sure you use a GCC compiler that supports C++11, e.g. GCC 4.8 or higher.
"""

# Read the contents of the requirements.txt file
with open("requirements.txt") as req_file:
    requirements = req_file.readlines()

setup(
    name="ABMShare",
    version="0.3.2",
    description="Based on Covasim and Synthpops by IDM COVID-19 Response Team",
    packages=find_packages(),
    include_package_data=True,  # Include files specified in MANIFEST.in
    install_requires=requirements,  # Use the contents of the requirements.txt file
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
)
