import pytest, json
from src import encors
from http import HTTPStatus

@pytest.fixture
def client():
    # setup testing client data
    encors.app.config['TESTING'] = True
    client = encors.app.test_client()

    yield client
    # clear testing client data before exit

# able to request at / 
def test_smoketest(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK

# able to request a test json from: http://www.pjliang.com/json/fake-users.json
def test_get_using_url(client):
    response = client.get('/http://www.pjliang.com/json/fake-users.json')
    assert response.status_code == HTTPStatus.OK
    assert response.content_type == 'application/json'
    json_object = json.loads(response.data)
    assert json_object[0]['name'] == 'Leanne Graham'

# able to request a test json from: http://www.pjliang.com/json/fake-users.json, using header
def test_get_using_header(client):
    headers = {
        'encors-target': 'http://www.pjliang.com/json/fake-users.json' 
    }
    response = client.post('/', data='', headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.content_type == 'application/json'
    json_object = json.loads(response.data)
    assert json_object[0]['name'] == 'Leanne Graham'
