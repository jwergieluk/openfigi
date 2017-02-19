#!/bin/bash

set -e; set -u

rm -f dist/*
python setup.py bdist_wheel sdist
cp dist/*.whl ${local_pypi}
dir2pi -n ${local_pypi} 

# twine upload dist/*
