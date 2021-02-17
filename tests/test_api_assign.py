from datetime import date, time

from src.accounting import db
from src.accounting.models import Job, Customer, Employee
from .helpers import add_customer, add_job, add_employee


def assign_customer_url(job_id):
    return f'/jobs/{job_id}/assign_customer'


def assign_employee_url(job_id):
    return f'/jobs/{job_id}/assign_employee'


def test_assign_customer_to_job_successfully(client):
    customer_id = add_customer('Stefan Miller', 11.5)
    job_id = add_job(date(2021, 11, 11), time(11, 30), 2.0)
    payload = {
        'customer_id': customer_id
    }

    res = client.post(assign_customer_url(job_id), json=payload)
    data = res.get_json()

    assert res.status_code == 201
    assert data['id'] == job_id
    assert data['date'] == '2021-11-11'
    assert data['start_time'] == '11:30:00'
    assert data['customer'] == {
        'id': 1,
        'name': 'Stefan Miller',
        'hourly_rate': 11.5
    }


def test_assign_customer_to_job_when_job_not_exists_fails(client):
    customer_id = add_customer('Stefan Miller', 11.5)
    payload = {
        'customer_id': customer_id
    }

    res = client.post(assign_customer_url(3), json=payload)
    data = res.get_json()

    assert res.status_code == 404
    assert data['error'] == 'Not Found'
    assert data['status'] == '404'
    assert data['method'] == 'POST'
    assert data['message'] == "A job doesn't exist."
    assert data['path'] == "/jobs/3/assign_customer"


def test_assign_customer_to_job_with_invalid_payload_fails(client):
    job_id = add_job(date(2021, 11, 11), time(11, 30), 2.0)
    payload = {
        'customer_id': ''
    }

    res = client.post(assign_customer_url(job_id), json=payload)
    data = res.get_json()

    assert res.status_code == 400
    assert data['error'] == 'Bad Request'
    assert data['status'] == '400'
    assert data['messages'] == {'customer_id': ['Not a valid integer.']}
    assert data['path'] == '/jobs/1/assign_customer'
    assert data['method'] == 'POST'


def test_assign_customer_to_job_when_customer_id_not_match(client):
    job_id = add_job(date(2021, 11, 11), time(11, 30), 2.0)
    payload = {
        'customer_id': 12
    }

    res = client.post(assign_customer_url(job_id), json=payload)
    data = res.get_json()

    assert res.status_code == 400
    assert data['error'] == 'Bad Request'
    assert data['status'] == '400'
    assert data['messages'] == {'customer_id': ['Not a matching integer.']}
    assert data['path'] == '/jobs/1/assign_customer'
    assert data['method'] == 'POST'


def test_assign_employee_to_job_successfully(client):
    employee_id = add_employee('Anna Testowa')
    job_id = add_job(date(2021, 1, 1), time(11, 30), 2.5)
    payload = {
        'employee_id': employee_id,
    }

    res = client.post(assign_employee_url(job_id), json=payload)
    data = res.get_json()

    assert res.status_code == 201
    assert data['id'] == job_id
    assert data['hours_number'] == 2.5
    assert data['employees'] == [{'id': 1, 'name': 'Anna Testowa'}]


def test_assign_employee_to_job_when_job_not_exists_fails(client):
    employee_id = add_employee('Anna Testowa')
    payload = {
        'employee_id': employee_id,
    }

    res = client.post(assign_employee_url(2), json=payload)
    data = res.get_json()

    assert res.status_code == 404
    assert data['error'] == 'Not Found'
    assert data['status'] == '404'
    assert data['method'] == 'POST'
    assert data['message'] == "A job doesn't exist."
    assert data['path'] == "/jobs/2/assign_employee"


def test_assign_employee_to_job_with_invalid_payload_fails(client):
    job_id = add_job(date(2021, 11, 11), time(11, 30), 2.0)
    payload = {
        'employee_id': ''
    }

    res = client.post(assign_employee_url(job_id), json=payload)
    data = res.get_json()

    assert res.status_code == 400
    assert data['error'] == 'Bad Request'
    assert data['status'] == '400'
    assert data['messages'] == {'employee_id': ['Not a valid integer.']}
    assert data['path'] == '/jobs/1/assign_employee'
    assert data['method'] == 'POST'


def test_assign_employee_to_job_when_employee_id_not_match(client):
    job_id = add_job(date(2021, 11, 11), time(11, 30), 2.0)
    payload = {
        'employee_id': 9
    }

    res = client.post(assign_employee_url(job_id), json=payload)
    data = res.get_json()

    assert res.status_code == 400
    assert data['error'] == 'Bad Request'
    assert data['status'] == '400'
    assert data['messages'] == {'employee_id': ['Not a matching integer.']}
    assert data['path'] == '/jobs/1/assign_employee'
    assert data['method'] == 'POST'
