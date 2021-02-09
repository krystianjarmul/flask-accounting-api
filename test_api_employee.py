import json

from app import app, Employee, db

EMPLOYEE_URL = '/employees/'


def add_employee(name):
    employee = Employee(name)
    db.session.add(employee)
    db.session.commit()


def test_retrieve_list_of_employees(client):
    attrs = {'name': 'Alina Testowska'}
    add_employee(attrs['name'])

    res = client.get(EMPLOYEE_URL)
    data = res.get_json()

    assert res.status_code == 200
    assert len(data) == 1
    assert data[0]['id'] == 1
    assert data[0]['name'] == attrs['name']
