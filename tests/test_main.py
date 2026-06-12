import json
import os
import time

import pytest
from fastapi.testclient import TestClient

from app.config import config
from app.main import app
from app.routers.optimizations import controller

# Create a test client using the FastAPI app
client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_optimizations():
    controller.optimizations.clear()


@pytest.fixture(autouse=True)
def load_config():
    path = os.path.join(os.path.dirname(__file__), '../config.properties')
    config.read(path)
    config.set('application', 'mode', 'ops')


@pytest.fixture
def data():
    path = os.path.join(os.path.dirname(__file__), '../dummy_data/scipy/test_data_11-weightings.json')
    with open(path, 'r') as f:
        data = json.load(f)
    return data


def test_post_optimization(data):
    # Check response when the optimization is created successfully
    response = client.post("/optimizations", json=data)
    assert response.status_code == 201


def test_post_and_get_optimization(data):
    # Check response when the optimization is created successfully
    response = client.post("/optimizations", json=data)
    response_data_post = response.json()
    assert response.status_code == 201

    # Get the optimization and check the content of the response
    response = client.get(f'/optimizations/{response_data_post["optimization_id"]}')
    response_data_get = response.json()
    assert response_data_get['optimization_id'] == response_data_post['optimization_id']
    assert response_data_get['status'] == 'CREATED'


def test_post_and_get_optimizations(data):
    # Check response when the optimization is created successfully
    response = client.post("/optimizations", json=data)
    response_data_post_one = response.json()
    assert response.status_code == 201

    response = client.post("/optimizations", json=data)
    response_data_post_two = response.json()
    assert response.status_code == 201

    # Get the optimization and check the content of the response
    response = client.get(f'/optimizations')
    response_data_get = response.json()
    assert len(response_data_get) == 2
    assert response_data_get[0]['optimization_id'] == response_data_post_one['optimization_id']
    assert response_data_get[0]['status'] == 'CREATED'
    assert response_data_get[1]['optimization_id'] == response_data_post_two['optimization_id']
    assert response_data_get[1]['status'] == 'CREATED'


def test_post_and_delete_optimization(data):
    # Check response when the optimization is created successfully
    response = client.post('/optimizations', json=data)
    response_data_post = response.json()
    assert response.status_code == 201

    response = client.delete(f'/optimizations/{response_data_post["optimization_id"]}')
    assert response.status_code == 200


def test_post_and_run_optimization_async(data):
    # Check response when the optimization is created successfully
    response = client.post('/optimizations', json=data)
    response_data_post = response.json()
    assert response.status_code == 201

    # Start the optimization run
    response = client.put(f'optimizations/{response_data_post["optimization_id"]}/start')
    assert response.status_code == 200

    # Check the status and results of the optimization
    response = client.get(f'optimizations/{response_data_post["optimization_id"]}')
    response_data_get = response.json()
    assert len(response_data_get['problem']['result_flight_lists']) == 0
    assert response_data_get['status'] == 'RUNNING'

    # Wait for the optimization to finish
    while True:
        response = client.get(f'optimizations/{response_data_post["optimization_id"]}')
        response_data_get = response.json()
        if response_data_get['status'] == 'FINISHED':
            break
        time.sleep(0.01)

    # Check the status and results of the optimization
    assert len(response_data_get['problem']['result_flight_lists']) != 0
    assert response_data_get['status'] == 'FINISHED'


def test_abort_optimization(data):
    # Check response when the optimization is created successfully
    response = client.post('/optimizations', json=data)
    response_data_post = response.json()
    assert response.status_code == 201

    # Start the optimization run
    response = client.put(f'optimizations/{response_data_post["optimization_id"]}/start')
    assert response.status_code == 200

    # Abort the optimization run
    response = client.put(f'optimizations/{response_data_post["optimization_id"]}/abort')
    assert response.status_code == 200

    response = client.get(f'optimizations/{response_data_post["optimization_id"]}')
    response_data_get = response.json()
    assert response_data_get['status'] == 'ABORTED'


def test_post_and_run_optimization_sync(data):
    # Check response when the optimization is created successfully
    response = client.post('/optimizations', json=data)
    response_data_post = response.json()
    assert response.status_code == 201

    # Start the optimization run
    response = client.put(f'optimizations/{response_data_post["optimization_id"]}/start/wait')
    assert response.status_code == 200

    # Check the status and results of the optimization
    response = client.get(f'optimizations/{response_data_post["optimization_id"]}')
    response_data_get = response.json()
    assert len(response_data_get['problem']['result_flight_lists']) != 0
    assert response_data_get['status'] == 'FINISHED'


def test_get_statistics(data):
    # Check response when the optimization is created successfully
    response = client.post('/optimizations', json=data)
    response_data_post = response.json()

    # Start the optimization run
    client.put(f'optimizations/{response_data_post["optimization_id"]}/start/wait')

    # Check the status and results of the optimization
    response = client.get(f'optimizations/{response_data_post["optimization_id"]}')
    response_data_get = response.json()
    assert response.status_code == 200
    assert response_data_get['statistics'] is not None
