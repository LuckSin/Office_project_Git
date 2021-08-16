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


def test_get_list_employees_as_admin(client):
    payload_admin = login_as_admin()
    response_login_admin = client.post('/api/v1/login', headers={'Content-Type': 'application/json'},
                                       data=payload_admin)
    response_employee = client.get('/api/v1/employees',
                                   headers=dict(
                                     Authorization='Bearer ' + json.loads(response_login_admin.data)['token'])
                                   )
    assert response_employee.status_code == 200


def test_get_list_employees_as_head_of_company(client):
    payload_admin = login_as_head_of_company()
    response_login_head_of_company = client.post('/api/v1/login',
                                                 headers={'Content-Type': 'application/json'},
                                                 data=payload_admin)
    response_employee = client.get('/api/v1/employees',
                                   headers=dict(Authorization='Bearer '
                                                              + json.loads(response_login_head_of_company.data)
                                                              ['token'])
                                   )
    assert response_employee.status_code == 200


def test_get_list_employees_as_head_of_employee(client):
    payload_admin = login_as_head_of_department()
    response_login_head_of_employee = client.post('/api/v1/login', headers={'Content-Type': 'application/json'},
                                                  data=payload_admin)
    response_employee = client.get('/api/v1/employees',
                                   headers=dict(Authorization='Bearer '
                                                              + json.loads(response_login_head_of_employee.data)
                                                              ['token'])
                                   )
    assert response_employee.status_code == 200


def test_get_list_employees_as_user(client):
    payload_admin = login_as_user()
    response_login_user = client.post('/api/v1/login', headers={'Content-Type': 'application/json'}, data=payload_admin)
    response_employee = client.get('/api/v1/employees',
                                   headers=dict(Authorization='Bearer '
                                                              + json.loads(response_login_user.data)
                                                              ['token'])
                                   )
    assert response_employee.status_code == 200
    assert response_employee.get_json()['Employee'] == [{'Department_id': 1, 'Full_name': 'staff', 'Login': 'User',
                                                         'Password': '12345678', 'Position_id': 5, 'Salary': '999.0',
                                                         'id': 24}]


def test_insert_employee_as_admin(client):
    payload = login_as_admin()
    response_login = client.post('/api/v1/login', headers={'Content-Type': 'application/json'}, data=payload)
    response_insert_employee = client.post('/api/v1/employee/create',
                                           data=json.dumps(dict(Department_id='7', Full_name='test_test',
                                                                Login='test_test', Password='123456789',
                                                                Position_id='5', Salary='123')),
                                           content_type='application/json',
                                           headers=dict(Authorization='Bearer ' +
                                                                      json.loads(response_login.data)['token'])
                                           )
    assert response_insert_employee.status_code == 200


def test_insert_employee_as_head_of_company(client):
    payload = login_as_head_of_company()
    response_login_head_of_company = client.post('/api/v1/login',
                                                 headers={'Content-Type': 'application/json'}, data=payload)
    response_insert_employee = client.post('/api/v1/employee/create',
                                           data=json.dumps(dict(Department_id='7', Full_name='test_test',
                                                                Login='test_test', Password='123456789',
                                                                Position_id='5', Salary='123')),
                                           content_type='application/json',
                                           headers=dict(Authorization='Bearer '
                                                                      + json.loads(response_login_head_of_company.data)
                                                                      ['token'])
                                           )
    assert response_insert_employee.status_code == 200


def test_insert_employee_as_head_of_employee(client):
    payload = login_as_head_of_department()
    response_login_head_of_employee = client.post('/api/v1/login',
                                                  headers={'Content-Type': 'application/json'}, data=payload)
    response_insert_employee = client.post('/api/v1/employee/create', data=json.dumps(dict(Department_id='7',
                                                                                           Full_name='test_test',
                                                                                           Login='test_test',
                                                                                           Password='123456789',
                                                                                           Position_id='5',
                                                                                           Salary='123')),
                                           content_type='application/json',
                                           headers=dict(Authorization='Bearer '
                                                                      + json.loads(response_login_head_of_employee.data)
                                                                      ['token'])
                                           )
    assert response_insert_employee.status_code == 200


def test_insert_employee_as_user(client):
    payload = login_as_user()
    response_login_user = client.post('/api/v1/login', headers={'Content-Type': 'application/json'}, data=payload)
    response_insert_employee = client.post('/api/v1/employee/create', data=json.dumps(dict(Department_id='7',
                                                                                           Full_name='test_test',
                                                                                           Login='test_test',
                                                                                           Password='123456789',
                                                                                           Position_id='5',
                                                                                           Salary='123')),
                                           content_type='application/json',
                                           headers=dict(Authorization='Bearer ' + json.loads(response_login_user.data)
                                                        ['token']))
    assert response_insert_employee.status_code == 200


def test_update_employee_as_admin(client):
    payload = login_as_admin()
    response_login = client.post('/api/v1/login', headers={'Content-Type': 'application/json'}, data=payload)
    response_update = client.put('/api/v1/employee/4/update', data=json.dumps(dict(Department_id='7',
                                                                                   Full_name='test_test',
                                                                                   Login='test_test',
                                                                                   Password='123456789',
                                                                                   Position_id='5',
                                                                                   Salary='123')),
                                 content_type='application/json',
                                 headers=dict(Authorization='Bearer ' + json.loads(response_login.data)['token']))
    assert response_update.status_code == 200


def test_update_employee_as_head_of_company(client):
    payload = login_as_head_of_company()
    response_login_head_of_company = client.post('/api/v1/login',
                                                 headers={'Content-Type': 'application/json'}, data=payload)
    response_update = client.put('/api/v1/employee/4/update', data=json.dumps(dict(Department_id='7',
                                                                                   Full_name='test_test',
                                                                                   Login='test_test',
                                                                                   Password='123456789',
                                                                                   Position_id='5',
                                                                                   Salary='123')),
                                 content_type='application/json',
                                 headers=dict(Authorization='Bearer '
                                                            + json.loads(response_login_head_of_company.data)['token']))
    assert response_update.status_code == 200


def test_update_employee_as_head_of_employee(client):
    payload = login_as_head_of_department()
    response_login_head_of_employee = client.post('/api/v1/login',
                                                  headers={'Content-Type': 'application/json'}, data=payload)
    response_update = client.put('/api/v1/employee/4/update', data=json.dumps(dict(Department_id='7',
                                                                                   Full_name='test_test',
                                                                                   Login='test_test',
                                                                                   Password='123456789',
                                                                                   Position_id='5',
                                                                                   Salary='123')),
                                 content_type='application/json',
                                 headers=dict(Authorization='Bearer '
                                                            + json.loads(response_login_head_of_employee.data)
                                                            ['token'])
                                 )
    assert response_update.status_code == 200


def test_update_employee_as_user(client):
    payload = login_as_user()
    response_login_user = client.post('/api/v1/login', headers={'Content-Type': 'application/json'}, data=payload)
    response_update = client.put('/api/v1/employee/4/update', data=json.dumps(dict(Department_id='7',
                                                                                   Full_name='test_test',
                                                                                   Login='test_test',
                                                                                   Password='123456789',
                                                                                   Position_id='5',
                                                                                   Salary='123')),
                                 content_type='application/json',
                                 headers=dict(Authorization='Bearer '
                                                            + json.loads(response_login_user.data)['token']))
    assert response_update.status_code == 200


def test_delete_employee_as_admin(client):
    payload = login_as_admin()
    response_login = client.post('/api/v1/login', headers={'Content-Type': 'application/json'}, data=payload)
    response_delete = client.delete('/api/v1/employee/9/delete',
                                    content_type='application/json',
                                    headers=dict(Authorization='Bearer ' + json.loads(response_login.data)['token']))
    assert response_delete.status_code == 200


def test_delete_employee_as_head_of_company(client):
    payload = login_as_head_of_company()
    response_login_head_of_company = client.post('/api/v1/login',
                                                 headers={'Content-Type': 'application/json'}, data=payload)
    response_delete = client.delete('/api/v1/employee/9/delete',
                                    content_type='application/json',
                                    headers=dict(Authorization='Bearer '
                                                               + json.loads(response_login_head_of_company.data)
                                                               ['token'])
                                    )
    assert response_delete.status_code == 200


def test_delete_employee_as_head_of_employee(client):
    payload = login_as_head_of_company()
    response_login_head_of_employee = client.post('/api/v1/login',
                                                  headers={'Content-Type': 'application/json'}, data=payload)
    response_delete = client.delete('/api/v1/employee/9/delete',
                                    content_type='application/json',
                                    headers=dict(Authorization='Bearer '
                                                               + json.loads(response_login_head_of_employee.data)[
                                                                   'token']))
    assert response_delete.status_code == 200


def test_delete_employee_as_user(client):
    payload = login_as_user()
    response_login_user = client.post('/api/v1/login',
                                      headers={'Content-Type': 'application/json'}, data=payload)
    response_delete = client.delete('/api/v1/employee/9/delete',
                                    content_type='application/json',
                                    headers=dict(Authorization='Bearer '
                                                               + json.loads(response_login_user.data)['token']))
    assert response_delete.status_code == 200
