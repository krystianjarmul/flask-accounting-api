from src.accountment.models import Employee
from src.accountment import db
from tests.helpers import add_employee

EMPLOYEE_URL = '/employees'


def detail_url(employee_id):
    return f'{EMPLOYEE_URL}/{employee_id}'


def test_retrieve_list_of_employees(client):
    add_employee('Alina Testowska')
    add_employee('Katarzyna Tester')
    add_employee('Teresa Testarossa')

    res = client.get(EMPLOYEE_URL)
    data = res.get_json()

    assert res.status_code == 200
    assert len(data) == 3


def test_retrieve_single_employee_successfully(client):
    employee_id = add_employee('Alina Testowska')

    res = client.get(detail_url(1))
    data = res.get_json()

    assert res.status_code == 200
    assert data['id'] == employee_id
    assert data['name'] == 'Alina Testowska'


def test_retrieve_single_employee_that_not_exists_fails(client):
    res = client.get(detail_url(2))
    data = res.get_json()

    assert res.status_code == 404
    assert data['error'] == 'Not Found'
    assert data['status'] == '404'
    assert data['method'] == 'GET'
    assert data['message'] == "An employee doesn't exist."
    assert data['path'] == "/employees/2"


def test_create_an_employee_successfully(client):
    payload = {
        'name': 'Agata Test'
    }

    res = client.post(EMPLOYEE_URL, json=payload)
    data = res.get_json()

    assert res.status_code == 201
    assert data['name'] == 'Agata Test'
    assert data['id'] == 1


def test_create_an_employee_with_invalid_payload_fails(client):
    payload = {
        'name': 3
    }

    res = client.post(EMPLOYEE_URL, json=payload)
    data = res.get_json()

    assert res.status_code == 400
    assert data['error'] == 'Bad Request'
    assert data['status'] == '400'
    assert data['method'] == 'POST'
    assert data['messages'] == {'name': ['Not a valid string.']}
    assert data['path'] == '/employees'


def test_create_an_employee_with_empty_payload_fails(client):
    payload = {}

    res = client.post(EMPLOYEE_URL, json=payload)
    data = res.get_json()

    assert res.status_code == 400
    assert data['error'] == 'Bad Request'
    assert data['status'] == '400'
    assert data['method'] == 'POST'
    assert data['messages'] == {'name': ['Missing data for required field.']}
    assert data['path'] == '/employees'


def test_update_an_employee_successfully(client):
    employee_id = add_employee('Alina Testowa')
    payload = {
        'name': 'Maria Test'
    }

    res = client.put(detail_url(employee_id), json=payload)
    data = res.get_json()

    assert res.status_code == 200
    assert data['name'] == payload['name']
    assert data['id'] == employee_id


def test_update_an_employee_with_invalid_payload_fails(client):
    employee_id = add_employee('Alina Testowa')
    payload = {
        'name': 12
    }

    res = client.put(detail_url(employee_id), json=payload)
    data = res.get_json()

    assert res.status_code == 400
    assert data['error'] == 'Bad Request'
    assert data['status'] == '400'
    assert data['method'] == 'PUT'
    assert data['messages'] == {'name': ['Not a valid string.']}
    assert data['path'] == '/employees/1'


def test_update_an_employee_with_empty_payload_fails(client):
    employee_id = add_employee('Maria Testerska')
    payload = {}

    res = client.put(detail_url(employee_id), json=payload)
    data = res.get_json()

    assert res.status_code == 400
    assert data['error'] == 'Bad Request'
    assert data['status'] == '400'
    assert data['method'] == 'PUT'
    assert data['messages'] == {'name': ['Missing data for required field.']}
    assert data['path'] == '/employees/1'


def test_update_an_employee_that_not_exists_fails(client):
    payload = {
        'name': 'Maria Test'
    }

    res = client.put(detail_url(5), json=payload)
    data = res.get_json()

    assert res.status_code == 404
    assert data['error'] == 'Not Found'
    assert data['status'] == '404'
    assert data['method'] == 'PUT'
    assert data['message'] == "An employee doesn't exist."
    assert data['path'] == "/employees/5"


def test_delete_an_employee_successfully(client):
    employee_id = add_employee('Alina Testowa')

    res = client.delete(detail_url(employee_id))
    data = res.get_json()

    assert res.status_code == 200
    assert data['name'] == 'Alina Testowa'


def test_delete_an_employee_that_not_exists_fails(client):
    res = client.delete(detail_url(5))
    data = res.get_json()

    assert res.status_code == 404
    assert data['error'] == 'Not Found'
    assert data['status'] == '404'
    assert data['method'] == 'DELETE'
    assert data['message'] == "An employee doesn't exist."
    assert data['path'] == "/employees/5"
