import pytest

from .login_test import *
from config import *


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.app_context():
        with app.test_client() as client:
            yield client


def test_login_as_admin(client):
    payload = login_as_admin()
    response_login = client.post('/api/v1/login', headers={'Content-Type': 'application/json'}, data=payload)
    data_login = json.loads(response_login.data)
    assert response_login.content_type == 'application/json'
    assert type(data_login['token']) == str
    assert response_login.status_code == 200


def test_login_as_head_of_company(client):
    payload = login_as_head_of_company()
    response_login = client.post('/api/v1/login', headers={'Content-Type': 'application/json'}, data=payload)
    data_login = json.loads(response_login.data)
    assert response_login.content_type == 'application/json'
    assert type(data_login['token']) == str
    assert response_login.status_code == 200


def test_login_as_head_of_department(client):
    payload = login_as_head_of_department()
    response_login = client.post('/api/v1/login', headers={'Content-Type': 'application/json'}, data=payload)
    data_login = json.loads(response_login.data)
    assert response_login.content_type == 'application/json'
    assert type(data_login['token']) == str
    assert response_login.status_code == 200


def test_login_as_user(client):
    payload = login_as_user()
    response_login = client.post('/api/v1/login', headers={'Content-Type': 'application/json'}, data=payload)
    data_login = json.loads(response_login.data)
    assert response_login.content_type == 'application/json'
    assert type(data_login['token']) == str
    assert response_login.status_code == 200


def test_get_list_departments_as_admin(client):
    payload_admin = login_as_admin()
    response_login_admin = client.post('/api/v1/login', headers={'Content-Type': 'application/json'},
                                       data=payload_admin)
    response_department = client.get('/api/v1/departments',
                                     headers=dict(
                                         Authorization='Bearer ' + json.loads(response_login_admin.data)['token']))
    assert response_department.status_code == 200


def test_get_list_departments_as_head_of_company(client):
    payload_admin = login_as_head_of_company()
    response_login_head_of_company = client.post('/api/v1/login', headers={'Content-Type': 'application/json'},
                                                 data=payload_admin)
    response_department = client.get('/api/v1/departments',
                                     headers=dict(Authorization='Bearer '
                                                                + json.loads(response_login_head_of_company.data)[
                                                                    'token']))
    assert response_department.status_code == 200


def test_get_list_departments_as_head_of_department(client):
    payload_admin = login_as_head_of_department()
    response_login_head_of_department = client.post('/api/v1/login', headers={'Content-Type': 'application/json'},
                                                    data=payload_admin)
    response_department = client.get('/api/v1/departments',
                                     headers=dict(Authorization='Bearer '
                                                                + json.loads(response_login_head_of_department.data)[
                                                                    'token']))
    assert response_department.status_code == 200


def test_get_list_departments_as_user(client):
    payload_admin = login_as_user()
    response_login_user = client.post('/api/v1/login', headers={'Content-Type': 'application/json'},
                                      data=payload_admin)
    response_department = client.get('/api/v1/departments',
                                     headers=dict(Authorization='Bearer '
                                                                + json.loads(response_login_user.data)['token']))
    assert response_department.status_code == 200
    assert response_department.get_json()['Department'] == {'Error': 'access denied'}


def test_insert_department_as_admin(client):
    payload = login_as_admin()
    response_login = client.post('/api/v1/login', headers={'Content-Type': 'application/json'}, data=payload)
    response_insert_department = client.post('/api/v1/department/create',
                                             data=json.dumps(dict(Office_id='2', Name='Accounting')),
                                             content_type='application/json',
                                             headers=dict(
                                                 Authorization='Bearer ' + json.loads(response_login.data)['token']))
    assert response_insert_department.status_code == 200


def test_insert_department_as_head_of_company(client):
    payload = login_as_head_of_company()
    response_login_head_of_company = client.post('/api/v1/login',
                                                 headers={'Content-Type': 'application/json'}, data=payload)
    response_insert_department = client.post('/api/v1/department/create',
                                             data=json.dumps(dict(Office_id='2', Name='Accounting')),
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer '
                                                                        +
                                                                        json.loads(response_login_head_of_company.data)
                                                                        ['token'])
                                             )
    assert response_insert_department.status_code == 200


def test_insert_department_as_head_of_department(client):
    payload = login_as_head_of_department()
    response_login_head_of_department = client.post('/api/v1/login',
                                                    headers={'Content-Type': 'application/json'}, data=payload)
    response_insert_department = client.post('/api/v1/department/create',
                                             data=json.dumps(dict(Office_id='2', Name='Accounting')),
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' +
                                                          json.loads(response_login_head_of_department.data)[
                                                              'token']))
    assert response_insert_department.status_code == 200


def test_insert_department_as_user(client):
    payload = login_as_user()
    response_login_user = client.post('/api/v1/login',
                                      headers={'Content-Type': 'application/json'}, data=payload)
    response_insert_department = client.post('/api/v1/department/create',
                                             data=json.dumps(dict(Office_id='2', Name='Accounting')),
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' +
                                                                        json.loads(response_login_user.data)['token'])
                                             )
    assert response_insert_department.status_code == 200


def test_update_department_as_admin(client):
    payload = login_as_admin()
    response_login = client.post('/api/v1/login', headers={'Content-Type': 'application/json'}, data=payload)
    response_update = client.put('/api/v1/department/2/update', data=json.dumps(dict(Office_id='2', Name='Accounting')),
                                 content_type='application/json',
                                 headers=dict(Authorization='Bearer ' + json.loads(response_login.data)['token']))
    assert response_update.status_code == 200


def test_update_department_as_head_of_company(client):
    payload = login_as_head_of_company()
    response_login_head_of_company = client.post('/api/v1/login', headers={'Content-Type': 'application/json'},
                                                 data=payload)
    response_update = client.put('/api/v1/department/6/update', data=json.dumps(dict(Office_id='2', Name='Accounting')),
                                 content_type='application/json',
                                 headers=dict(Authorization='Bearer '
                                                            + json.loads(response_login_head_of_company.data)['token']))
    assert response_update.status_code == 200


def test_update_department_as_head_of_department(client):
    payload = login_as_head_of_department()
    response_login_head_of_department = client.post('/api/v1/login', headers={'Content-Type': 'application/json'},
                                                    data=payload)
    response_update = client.put('/api/v1/department/6/update', data=json.dumps(dict(Office_id='2', Name='Accounting')),
                                 content_type='application/json',
                                 headers=dict(Authorization='Bearer '
                                                            + json.loads(response_login_head_of_department.data)
                                                            ['token'])
                                 )
    assert response_update.status_code == 200


def test_update_department_as_user(client):
    payload = login_as_user()
    response_login_user = client.post('/api/v1/login', headers={'Content-Type': 'application/json'}, data=payload)
    response_update = client.put('/api/v1/department/6/update', data=json.dumps(dict(Office_id='2', Name='Accounting')),
                                 content_type='application/json',
                                 headers=dict(Authorization='Bearer '
                                                            + json.loads(response_login_user.data)['token']))
    assert response_update.status_code == 200


def test_delete_department_as_admin(client):
    payload = login_as_admin()
    response_login = client.post('/api/v1/login', headers={'Content-Type': 'application/json'}, data=payload)
    response_delete = client.delete('/api/v1/department/7/delete',
                                    content_type='application/json',
                                    headers=dict(Authorization='Bearer ' + json.loads(response_login.data)['token']))
    assert response_delete.status_code == 200


def test_delete_department_as_head_of_company(client):
    payload = login_as_head_of_company()
    response_login_head_of_company = client.post('/api/v1/login',
                                                 headers={'Content-Type': 'application/json'}, data=payload)
    response_delete = client.delete('/api/v1/department/8/delete',
                                    content_type='application/json',
                                    headers=dict(Authorization='Bearer '
                                                               + json.loads(response_login_head_of_company.data)[
                                                                   'token']))
    assert response_delete.status_code == 200


def test_delete_department_as_head_of_department(client):
    payload = login_as_head_of_company()
    response_login_head_of_department = client.post('/api/v1/login',
                                                    headers={'Content-Type': 'application/json'}, data=payload)
    response_delete = client.delete('/api/v1/department/9/delete',
                                    content_type='application/json',
                                    headers=dict(Authorization='Bearer '
                                                               + json.loads(response_login_head_of_department.data)[
                                                                   'token']))
    assert response_delete.status_code == 200


def test_delete_department_as_user(client):
    payload = login_as_user()
    response_login_user = client.post('/api/v1/login',
                                      headers={'Content-Type': 'application/json'}, data=payload)
    response_delete = client.delete('/api/v1/department/11/delete',
                                    content_type='application/json',
                                    headers=dict(Authorization='Bearer '
                                                               + json.loads(response_login_user.data)['token']))
    assert response_delete.status_code == 200
