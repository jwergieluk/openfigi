#!/bin/bash

set -e; set -u

pandoc -f markdown -t rst -o README.rst README.md

python setup.py bdist_wheel sdist
cp dist/*.whl ${local_pypi}
dir2pi -n ${local_pypi} 

# twine upload dist/*
