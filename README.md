# Documentation

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Local Development Setup

## Environment Variables

We are using `dotenv` package to utilize environment variables in this project. Refer to `.env.example` file in the repo to see the existing environment variables. Then make a new copy of this file and rename it to `.env` in the root of the project.

## Tests:

Test scripts are located in `manage.py > tests`. To run the tests you have three options to run them. You must have following environment variable set before running tests from the comand line:

```bash
export FLASK_APP=manage.py

```

1. Following syntax will run all the tests and generates the coverage report.

   ```bash
   flask tests
   ```

2. Running in **watch** mode: will keep your tests watching for changes and run them
   ```bash
   flask tests watch
   ```
3. Running in **debug** mode: will prompt you to debugging console if any error is thrown during running tests
   ```bash
   flask tests debug
   ```

# Architecture Overview

# Code Overview

# Algorithmic Complexity

# Instruction Nn How To Run The Proxy And Tests

# List of Not Imlemented Requirements
