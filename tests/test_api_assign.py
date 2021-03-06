from datetime import date, time

from src.accountment import db
from src.accountment.models import Job, Customer, Employee
from .helpers import add_customer, add_job, add_employee, assign_customer, \
    assign_employee


def detail_job_url(job_id):
    return f'/jobs/{job_id}'


def assign_employee_url(job_id):
    return f'/jobs/{job_id}/assignment'


def unassign_employee_url(job_id):
    return f'jobs/{job_id}/unassignment'


def test_assign_customer_to_job_successfully(client):
    customer_id = add_customer('Stefan Miller', 11.5)
    job_id = add_job(date(2021, 11, 11), time(11, 30), 2.0)
    payload = {
        'customer_id': customer_id
    }

    res = client.patch(detail_job_url(job_id), json=payload)
    data = res.get_json()

    assert res.status_code == 200
    assert data['id'] == job_id
    assert data['date'] == '2021-11-11'
    assert data['start_time'] == '11:30:00'
    assert data['customer'] == {
        'id': 1,
        'name': 'Stefan Miller',
        'hourly_rate': 11.5
    }


def test_assign_customer_to_job_when_customer_id_not_match(client):
    job_id = add_job(date(2021, 11, 11), time(11, 30), 2.0)
    payload = {
        'customer_id': 12
    }

    res = client.patch(detail_job_url(job_id), json=payload)
    data = res.get_json()

    assert res.status_code == 400
    assert data['error'] == 'Bad Request'
    assert data['status'] == '400'
    assert data['messages'] == {'customer_id': ['Not a matching integer.']}
    assert data['path'] == f'/jobs/{job_id}'
    assert data['method'] == 'PATCH'


def test_assign_customer_to_job_when_job_not_exists_fails(client):
    customer_id = add_customer('Stefan Miller', 11.5)
    payload = {
        'customer_id': customer_id
    }

    res = client.patch(detail_job_url(3), json=payload)
    data = res.get_json()

    assert res.status_code == 404
    assert data['error'] == 'Not Found'
    assert data['status'] == '404'
    assert data['method'] == 'PATCH'
    assert data['message'] == "A job doesn't exist."
    assert data['path'] == '/jobs/3'


def test_assign_customer_to_job_with_invalid_payload_fails(client):
    job_id = add_job(date(2021, 11, 11), time(11, 30), 2.0)
    payload = {
        'customer_id': ''
    }

    res = client.patch(detail_job_url(job_id), json=payload)
    data = res.get_json()

    assert res.status_code == 400
    assert data['error'] == 'Bad Request'
    assert data['status'] == '400'
    assert data['messages'] == {'customer_id': ['Not a valid integer.']}
    assert data['path'] == f'/jobs/{job_id}'
    assert data['method'] == 'PATCH'


def test_reassign_customer_from_job_successfully(client):
    job_id = add_job(date(2021, 11, 11), time(11, 30), 2.0)
    customer_id1 = add_customer('Stefan Miller', 12.0)
    customer_id2 = add_customer('Michael Jordan', 11.5)
    assign_customer(job_id, customer_id1)
    payload = {
        'customer_id': customer_id2
    }

    res = client.patch(detail_job_url(job_id), json=payload)
    data = res.get_json()

    assert res.status_code == 200
    assert data['id'] == job_id
    assert data['customer'] == {
        'id': 2,
        'name': 'Michael Jordan',
        'hourly_rate': 11.5
    }


def test_assign_employee_to_job_successfully(client):
    customer_id = add_customer('Micheal Jordan', 11.5)
    employee_id = add_employee('Anna Testowa')
    job_id = add_job(date(2021, 1, 1), time(11, 30), 2.5)
    assign_customer(job_id, customer_id)
    payload = {
        'employee_id': employee_id,
    }

    res = client.post(assign_employee_url(job_id), json=payload)
    data = res.get_json()

    assert res.status_code == 200
    assert data['id'] == job_id
    assert data['hours_number'] == 2.5
    assert data['employees'] == [
        {
            'id': 1,
            'name': 'Anna Testowa',
            'hours_number': 2.5,
            'payment': 28.75
        }
    ]


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
    assert data['path'] == assign_employee_url(2)


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
    assert data['path'] == assign_employee_url(job_id)
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
    assert data['path'] == assign_employee_url(job_id)
    assert data['method'] == 'POST'


def test_unassign_employee_from_job_successfully(client):
    employee_id1 = add_employee('Maria Nowak')
    employee_id2 = add_employee('Katarzyna Test')
    job_id = add_job(date(2021, 11, 1), time(11, 30), 2.5)
    assign_employee(job_id, employee_id1)
    assign_employee(job_id, employee_id2)
    payload = {
        'employee_id': employee_id1,
    }

    res = client.post(unassign_employee_url(job_id), json=payload)
    data = res.get_json()

    assert res.status_code == 200
    assert data['id'] == job_id
    assert data['employees'] == [
        {
            'id': 2,
            'name': 'Katarzyna Test',
            'hours_number': 2.5,
            'payment': 0
        }
    ]
