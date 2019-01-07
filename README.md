flask-redis-docker
==================

An example about how to deploy a Flask application inside a Docker able to perform
asynchronous, parallel requests, with the Flask application handled by NGINX/uWSGI.

How it works
------------

Though Python allows asynchronous executions through several techniques, forking
asynchronous processes from the uWSGI plugin is not allowed (at least by default),
and not recommended (see https://docs.docker.com/config/containers/multi-service_container/).
A good solution is to define a `worker` process within the main processes of the container
(i.e. handled through `supervisor`, used as main process defined in the container's
`CMD`), that is able to perform operations in background.

The repo has two sections, one dedicated to Python 2.7 (based on `RedisQueue`) and
one to Python 3.6 (based on `Celery`). Both examples use `Redis` as broker messages.

How to run it
-------------

Once you have `docker-compose` installed, just create the images and the containers
through the command:

```
$ docker-compose up -d

```

This will create the two containers, the one with the Flask application listening
port `5000`, and the one with the `Redis` service (listening port `6379`).

```
$ docker-compose ps
 Name               Command               State               Ports            
-------------------------------------------------------------------------------
redis    docker-entrypoint.sh redis ...   Up      6379/tcp                     
webapp   /entrypoint.sh /start.sh         Up      443/tcp, 0.0.0.0:5000->80/tcp
```

Once both services are up and running in your localhost, you can submit a long running
request asynchronously as follows:

```
$ curl -X POST -F "duration=20" http://127.0.0.1:5000/long_task
```

and for a parallelised task:

```
$ curl -X POST -F "duration=200" http://127.0.0.1:5000/parallel_long_task
```

Then the outputs can be retrieved as follows:

```
$ curl -X GET http://127.0.0.1:5000/task/<task_id>
```

or, in the case of a parallel task:

```
$ curl -X GET http://127.0.0.1:5000/parallel_task/<task_id>
```
