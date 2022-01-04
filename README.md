[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A transparent Reids proxy service providing a local caching layer with GET requests.

# Assumptions

I assumed that the Backing Redis acts as a permanenet database and the keys will not be deleted after expiry.

# Getting Started

After cloning the repository, cd into `redis-proxy` and run `make test`, assuming that you have installed:

- [make](https://www.gnu.org/software/make/)
- [docker](https://www.docker.com/get-started)

```bash
# clone
git clone git@github.com:amirsalaar/redis-proxy.git

# change directory
cd <path-to-where-you-cloned-the-repo>/redis-proxy

# Single click build and test. Make sure Docker host is running on your machine
make test
```

For stopping the service simply run `make stop`.

## Configuration

The following parameters are configurable at the proxy startup in `.env` file:

- Address of the backing Redis: `REDIS_ADDRESS`
- Cache expiry time: `GLOBAL_CACHE_EXPIRY` (in secods)
- Cache capacity (number of keys): `CACHE_CAPACITY`
- TCP/IP address and port the proxy listens on: `FLASK_RUN_HOST` and `FLASK_RUN_PORT`

## API Usage:

Before using the API, run the following command to seed the Backing Redis with some seed data so that you can test the API (make sure the services are running: `make run`):

```bash
# OPTIONAL: if you havent build the services yet
make build

# OPTIONAL: if the services are not running yet
make run

# seeds some keys to Backing Redis --> key format: seeded_key{i}
make seed

# OPTIONAL: if you want to stop the services
make
```

### Endpoint

- GET `/proxy?key=your-key`

  - query_parameter: `key`
  - Example: GET `/proxy?key=seeded_key1`

# High-Level Architecture And Code Overview

Three different componenets have been considered in designing this distributed system.

1. Local Cache
2. Backing Redis Instance
3. HTTP Proxy Server

`utilities` also contains some shared logic for the project:

- Utilities
  - app_logger
  - error_handler

## 1. Local Cache

`LocalCache` class is an LRU cache which takes two required args to instantiate the class, `capacity` and `global_expiry`.

A shared global in-memory instance of `LocalCache` class will be instantiated in the app and handed over to the `ProxyServer` class.

Following ENV vars can be set up before running the system as enviroment variables in the `.env` file:

1. `CACHE_CAPACITY`: This will determine the capacity of your LRU cache.
2. `GLOBAL_CACHE_EXPIRY`: This will determine the global expiry of the LRU cache. I assumed that the expiry will be used in **seconds**.

### LRU Cache

The LRU cache was implemented using an `OrderedDict` in Python and it is utilized in `cache.py` module.

### Concurrent Access Management

For concurrent access management, a mutual exclusion object was used, named `cache_locker`. The `cache_locker` is basically a mutex that manages the thread access and makes sure for each `GET` and `SET` request to the in-memory cache, the thread is ready to handle the operation.

### Global Expiry Implementation

At the time of setting a new key-value pair in the cache, an expiry time (in seconds will be added to the object that is going to be cached. On key retrieving event, if the time has passed from the original expiry, we remove it from the local cache and return `None`.

## 2. Backing Redis Instance

The Redis instance will be instantiated along with the server and assuming that both of the server and Redis isntance are on the same Docker host, no IP address was used to refer to the redis instance. I have defaulted the Backing Redis instance to `redis:6379` in the `.env` file but you can configure it to any Redis instance outside the Docker host by setting the following ENV var inside the `.env`:

```
REDIS_ADDRESS=redis:6379
```

For example, when running the tests locally and developing the project, you can set it to `localhost:6379`.

## 3. HTTP Proxy Server

The Proxy server will communicate between the Backing Redis instance and the Local Cache.

### Service

The services module holds the logic for retrieving the data from cache. `ProxyService` will be i charge of handling this retrieval logic.

### Controller

The controller module holds the logic for communicating with the endpoints. It also instantiate a global in-memoery `local_cache` which will be sent to the `ProxyService` class. This is to avoid reinstantiation of a new cache on each request to the `proxy` endpoint.

## 4. Utilities

- App Logger: A simple custom app logger has been implemented that collects the logs of the application and puts it into `applogs.log`.
  - These logs are handy when you want to see if a key has been retrieved from the local cache or backing redis
- Custom Error Handler: A custom error handler has been implemented to return a unified error to the proxy consumers with traceback and a proper message. For example, if a key is requested which is not inside the cache, a `NotFound` error will be raised, handled, and retrned to the user.

# Algorithmic Complexity

A built-in python OrederedDict has been used in the implementation of the LRU. Similar to dictionaries, the `get` and `set` method to retrieve and put a key value is of O(1) time complexity. The space complexity depdends on the value that has been stored initially. When looking up the Backing Redis for a key value the time complexity will be still O(1).

# Local Development

Make sure that you are mirroring the redis address to localhost in the `.env` file and comment `FLASK_ENV=production` since this is a checker in the e2e tests to switch to `redis:6379` address.

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

# Time Spent On Each Part of the Project

1. Reading the specs and understanding it: A couple of hours or maybe an hour
2. Setting up the whole project skleton: few hours of a day after work
3. Breaking down the tasks needed to be done and breaking the components need to be developed: An hour
4. Developing the local cache and LRU cache and their unit tests: about 3 to 4 hours
5. Developing the client for setting up the communication with the backing redis with their unit test: less than an hour
6. Developing the HTTP proxy server and its service and controller with their unit tests: about a day
7. Developing utilities of the project and testing them: 2 to 3 hours
8. Writing e2e test: few hours
9. Making the project work with a single click build and test with `make`: les than an hour
10. Developing the Dockerfile, and docker-compose.yaml for orchestrating the docker containers: an hour or two
11. Writing up documentations: about 2 hours

# A list of the missing requirements:

- The bonus points:
  - Parallel concurrent processing
  - Concurrent client limit
  - Redis client protocol
