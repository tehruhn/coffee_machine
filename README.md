# Python Coffee Machine

Implements a coffee machine in Python for the task given by Humit.

## Sample Usage

Run the `sample_usage.py` file inside the `coffee_machine` directory using :
```
python3 sample_usage.py
```
This replicates the sample output as requested in the design document.

## Running tests

`pytest` is required for running tests. Install it using :
```
pip3 install pytest
```
Run the following command inside the `coffee_machine` directory:
```
pytest -v
```

## Test coverage

`pytest-cov` is used for generating coverage, and it is currently at 100%. Install using:
```
pip3 install pytest-cov
```
Run the following exactly to see the code coverage from inside the `coffee_machine` directory:
```
pytest --cov=coffee_machine
```