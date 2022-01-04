# Documentation

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Architecture Overview

Three different componenets have been considered in designing this distributed system.

1. Local Cache
2. Backing Redis Instance
3. HTTP Proxy Server
4. Utilities
   - app_logger
   - error_handler

## 1. Local Cache

`LocalCache` module is an LRU cache with two global configuration that can be set up before running the system as enviroment variables in the `.env` file.

1. `CACHE_CAPACITY`: This will determine the capacity of your LRU cache.
2. `GLOBAL_CACHE_EXPIRY`: This will determine the global expiry of the LRU cache. I assumed that the expiry will be used in **seconds**.

### LRU Cache

The LRU cache was implemented using an OrderedDict in Python and it is utilized in `cache.py` module.

## 2. Backing Redis Instance

The Redis instance will be instantiated along with the server and assuming that both of the server and Redis isntance are on the same Docker host, no IP address was used to refer to the redis instance. I have defaulted the Backing Redis instance to `redis:6379` in the `.env` file but you can configure it to any Redis instance by setting the following ENV var inside the `.env`:

- `REDIS_ADDRESS=redis:6379`

## 3. HTTP Proxy Server

The Proxy server will communicate between the Backing Redis instance and the Local Cache.

## 4. Utilities

- App Logger: A simple custom app logger has been implemented that collects the logs of the application and puts it into `applogs.log`.
  - These logs are handy when you want to see if a key has been retrieved from the local cache or backing redis
- Custom Error Handler: A custom error handler has been implemented to return a unified error to the proxy consumers with traceback and a proper message.

# Code Overview

For concurrent access management, a mutual exclusion object was used. I had no previous experience with such a concept and that was agreat learning moment for me. This ended me up becoming familiar with `mutex` and `semaphore`.

- `mutex`: An oject is created so that multiple program thread can take turns sharing the same resource. It is a **locking mechanism**.
- `semaphore`: It is a signaling mechanism.

The mutex object in Python has been implemented using the threading module by locking the thread to wait for the current thread to finish first before proceeding to the next thread. In the `CacheContainer` class, `locker` has been used as mutex to manage the locking and thread.

## Expiry Implementation

At the time of setting a new key-value pair in the cache, an expiry in seconds will be added to the object that is going to be cached. On retrieving the cached key, if the time has passed from the expiry, we remove it from the Cache and return `None`.

# Algorithmic Complexity

A built-in python OrederedDict has been used in the implementation of the LRU. Similar to dictionaries, the `get` and `set` method to retrieve and put a key value is of O(1) time complexity. The space complexity depdends on the value that has been stored initially. When looking up the Backing Redis for a key value the time complexity will be still O(1).

# Configuration

The following parameters are configurable at the proxy startup in `.env` file:

- Address of the backing Redis: `REDIS_ADDRESS`
- Cache expiry time: `GLOBAL_CACHE_EXPIRY` (in secods)
- Cache capacity (number of keys): `CACHE_CAPACITY`
- TCP/IP address and port the proxy listens on: `FLASK_RUN_HOST` and `FLASK_RUN_PORT`

# Instruction On How To Run The Proxy And Tests

# List of Not Imlemented Requirements

# Assumptions

I assumed that the Backing Redis acts as a permanenet database and the data wont be deleted from it after expiry.

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
