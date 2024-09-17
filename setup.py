# -*- coding: utf-8 -*-
"""Setup file"""

import os
import sys
from typing import Dict
from setuptools import setup, find_packages


NAME = "challenge"
SCRIPT = ["main.py"]
DESCRIPTION = "A FastAPI application for challenge"

here = os.path.abspath(os.path.dirname(__file__))

version: Dict = {}
version_file = os.path.join(here, "challenge/version.py")
if os.path.exists(version_file):
    with open(version_file) as fp:
        exec(fp.read(), version)
else:
    version["__version__"] = "0.10.1"

unit_deps = []
requirements_file = os.path.join(here, "requirements.txt")
if os.path.exists(requirements_file):
    with open(requirements_file) as fp:
        unit_deps = fp.readlines()

test_deps = []
requirements_test_file = os.path.join(here, "requirements-test.txt")
if os.path.exists(requirements_test_file):
    with open(requirements_test_file) as fp:
        test_deps = fp.readlines()

setup(
    name=NAME,
    version=version["__version__"],
    url="https://github.com/AguadaC/fastApi-app",
    license="MIT",
    author="Cristian Aguada",
    author_email="aguadacristian@gmail.com",
    description=DESCRIPTION,
    long_description="Application to manage lead in a DB",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Framework :: FastAPI",
        "Environment :: Console",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    scripts=SCRIPT,
    install_requires=unit_deps,
    tests_require=test_deps,
    setup_requires=["pytest-runner"] if "test" in sys.argv else [],
    entry_points={
        "console_scripts": [
            f"{NAME} = main:run_dev_server",
        ],
    },
)
