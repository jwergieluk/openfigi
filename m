#!/bin/bash

set -e; set -u

python setup.py bdist_wheel
cp dist/*.whl ${local_pypi}
dir2pi -n ${local_pypi} 

