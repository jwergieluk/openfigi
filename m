#!/bin/bash

set -e; set -u

rm -f dist/*
python setup.py bdist_wheel sdist
twine upload dist/*

