import json

from app import app, Employee, db

EMPLOYEE_URL = '/employees/'


def detail_url(employee_id):
    return f'{EMPLOYEE_URL}{employee_id}'


def add_employee(name):
    employee = Employee(name)
    db.session.add(employee)
    db.session.commit()


def test_retrieve_list_of_employees(client):
    add_employee('Alina Testowska')
    add_employee('Katarzyna Tester')
    add_employee('Teresa Testarossa')

    res = client.get(EMPLOYEE_URL)
    data = res.get_json()

    assert res.status_code == 200
    assert len(data) == 3


def test_retrieve_single_employee_successful(client):
    add_employee('Alina Testowska')

    res = client.get(detail_url(1))
    data = res.get_json()

    assert res.status_code == 200
    assert data['id'] == 1
    assert data['name'] == 'Alina Testowska'


def test_retrieve_single_employee_fails(client):
    res = client.get(detail_url(2))

    assert res.status_code == 404
    assert b'An employee does not exist' in res.data


def test_create_an_employee_successful(client):
    payload = {
        'name': 'Agata Test'
    }

    res = client.post(EMPLOYEE_URL, json=payload)
    data = res.get_json()

    assert res.status_code == 201
    assert data['name'] == 'Agata Test'


def test_create_an_employee_with_invalid_payload(client):
    payload = {
        'name': ''
    }

    res = client.post(EMPLOYEE_URL, json=payload)
    data = res.get_json()

    assert res.status_code == 400
    assert b'No name was given' in res.data
