from celery import Celery

from flask import Flask, request, jsonify

from long_task_package.long_task import long_task
from long_task_package.long_task import parallel_long_task

app = Flask(__name__)
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'
app.config['CELERY_BACKEND_URL'] = 'redis://redis:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BACKEND_URL'])
celery.conf.update(app.config)

@celery.task(bind=True)
def wrap_long_task(self, task_duration):
    return long_task(task_duration)

@celery.task(bind=True)
def wrap_parallel_long_task(self, task_duration):
    return parallel_long_task(task_duration)

@app.route('/long_task', methods=['POST'])
def run_long_task():
    task_duration = int(request.form['duration'])

    task = wrap_long_task.apply_async(args=[task_duration])
    response_object = {
        'status': 'success',
        'data': {
            'task_id': task.id
        }
    }
    return jsonify(response_object), 202


@app.route('/parallel_long_task', methods=['POST'])
def run_parallel_long_task():
    task_duration = int(request.form['duration'])

    task = wrap_parallel_long_task.apply_async(args=[task_duration])
    response_object = {
        'status': 'success',
        'data': {
            'task_id': task.id
        }
    }
    return jsonify(response_object), 202


@app.route('/task/<task_id>', methods=['GET'])
def get_task_status(task_id):
    task = wrap_long_task.AsyncResult(task_id)

    response = {
        'status': task.state,
        'result': 'not finished yet'
    }

    if task.state != 'FAILURE' and task.state != 'PENDING':
        response = {
            'status': task.state,
            'result': task.info
        }
    elif task.state == 'FAILURE':
        response = {
            'status': task.state,
            'result': str(task.info)
        }

    return jsonify(response)


@app.route('/parallel_task/<task_id>', methods=['GET'])
def get_parallel_task_status(task_id):
    task = wrap_parallel_long_task.AsyncResult(task_id)

    response = {
        'status': task.state,
        'result': 'not finished yet'
    }

    if task.state != 'FAILURE' and task.state != 'PENDING':
        response = {
            'status': task.state,
            'result': task.info
        }
    elif task.state == 'FAILURE':
        response = {
            'status': task.state,
            'result': str(task.info)
        }

    return jsonify(response)



if __name__ == '__main__':
    # Only for debugging while developing
    # app.run(host='0.0.0.0', debug=True, port=80)
    pass
