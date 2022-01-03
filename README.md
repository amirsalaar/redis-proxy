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

Three different componenets have been considered in designing this distributed system.

1. Local Cache
2. Backing Redis Instance
3. HTTP Proxy Server

## 1. Local Cache

`LocalCache` module is an LRU cache with two global configuration that can be set up before running the system as enviroment variables in the `.env` file.

1. `CACHE_CAPACITY`: This will determine the capacity of your LRU cache.
2. `GLOBAL_CACHE_EXPIRY`: This will determine the global expiry of the LRU cache. I assumed that the expiry will be used in **seconds**.

### LRU Cache

The LRU cache was implemented using an OrderedDict in Python and it is utilized in `cache.py` module.

## 2. Backing Redis Instance

The Redis instance will be instantiated along with the server and assuming that both of the server and Redis isntance are on the same Docker host, no IP address was used to refer to the redis instance. I have defaulted the Backing Redis instance to `redis:6379` in the `.env` file but you can configure it to any Redis instance by setting the following ENV var inside the `.env`:

- `REDIS_ADDRESS=redis:6379`

# Code Overview

# Algorithmic Complexity

# Instruction On How To Run The Proxy And Tests

# List of Not Imlemented Requirements
