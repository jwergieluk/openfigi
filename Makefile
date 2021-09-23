export PYTHONPATH = .

black-format:
	black -t py38 -S -l 120 openfigi tests setup.py

black: black-format

test:
	pytest -v tests

