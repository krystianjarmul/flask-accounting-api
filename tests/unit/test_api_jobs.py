from datetime import time, date

from tests.helpers import add_job, add_customer, add_employee

JOBS_URL = '/jobs'


def detail_url(job_id):
    return f'{JOBS_URL}/{job_id}'


def test_retrieve_list_of_jobs(client):
    add_job(1, [2, 3], date(2021, 1, 1), time(11, 30), 2.0)
    add_job(2, [1], date(2021, 2, 1), time(10, 30), 2.5)
    add_job(3, [4, 5], date(2021, 1, 3), time(11, 00), 1.0)

    res = client.get(JOBS_URL)
    data = res.get_json()

    assert res.status_code == 200
    assert len(data) == 3


def test_retrieve_a_single_job_successfully(client):
    employee1_id = add_employee('Anna Testowska')
    employee2_id = add_employee('Maria Tester')
    customer_id = add_customer('Michael Ballack', 12.0)
    job_id = add_job(1, [2, 3], date(2021, 1, 1), time(11, 30), 2.0)

    res = client.get(detail_url(job_id))
    data = res.get_json()

    assert res.status_code == 200
    assert data['id'] == job_id
    assert data['date'] == '2021-01-01'
    assert data['employee_ids'] == '2,3'
    assert data['start_time'] == '11:30:00'
    assert data['hours_number'] == 2.0
    assert data['customer'] == {
        'id': 1,
        'name': 'Michael Ballack',
        'hourly_rate': 12.0
    }


def test_retrieve_a_single_job_that_not_exists_fails(client):
    res = client.get(detail_url(2))
    data = res.get_json()

    assert res.status_code == 404
    assert data['error'] == 'Not Found'
    assert data['status'] == '404'
    assert data['method'] == 'GET'
    assert data['message'] == "A job doesn't exist."
    assert data['path'] == "/jobs/2"


def test_create_a_job_successfully(client):
    payload = {
        'customer_id': 1,
        'employee_ids': '2,3',
        'date': '2021-02-02',
        'start_time': '10:30:00',
        'hours_number': 1.5,
    }

    res = client.post(JOBS_URL, json=payload)
    data = res.get_json()

    assert res.status_code == 201
    assert data['id'] == 1
    assert data['customer_id'] == payload['customer_id']
    assert data['employee_ids'] == payload['employee_ids']
    assert data['date'] == payload['date']
    assert data['start_time'] == payload['start_time']
    assert data['hours_number'] == payload['hours_number']


def test_create_a_job_with_invalid_payload_fails(client):
    payload = {
        'customer_id': '',
        'employee_ids': '2,3',
        'date': '2021-02-02',
        'start_time': '10:30:00',
        'hours_number': 1.5,
    }

    res = client.post(JOBS_URL, json=payload)
    data = res.get_json()

    assert res.status_code == 400
    assert data['error'] == 'Bad Request'
    assert data['status'] == '400'
    assert data['method'] == 'POST'
    assert data['messages'] == {'customer_id': ['Not a valid integer.']}
    assert data['path'] == "/jobs"


def test_create_a_job_with_empty_payload_fails(client):
    payload = {}

    res = client.post(JOBS_URL, json=payload)
    data = res.get_json()

    assert res.status_code == 400
    assert data['error'] == 'Bad Request'
    assert data['status'] == '400'
    assert data['method'] == 'POST'
    assert data['messages'] == {
        'customer_id': ['Missing data for required field.'],
        'date': ['Missing data for required field.'],
        'employee_ids': ['Missing data for required field.'],
        'hours_number': ['Missing data for required field.'],
        'start_time': ['Missing data for required field.']
    }
    assert data['path'] == "/jobs"


def test_partial_update_successfully(client):
    job_id = add_job(1, [2, 3], date(2021, 1, 1), time(11, 30), 2.0)
    payload = {
        'hours_number': 1.5,
    }

    res = client.patch(detail_url(job_id), json=payload)
    data = res.get_json()

    assert res.status_code == 200
    assert data['id'] == job_id
    assert data['hours_number'] == 1.5


def test_partial_update_with_invalid_payload_fails(client):
    job_id = add_job(1, [2, 3], date(2021, 1, 1), time(11, 30), 2.0)
    payload = {
        'date': 2011.1011,
    }

    res = client.patch(detail_url(job_id), json=payload)
    data = res.get_json()

    assert res.status_code == 400
    assert data['error'] == 'Bad Request'
    assert data['status'] == '400'
    assert data['messages'] == {'date': ['Not a valid date.']}
    assert data['path'] == '/jobs/1'
    assert data['method'] == 'PATCH'


def test_partial_update_job_that_not_exists_fails(client):
    payload = {
        'customer_id': 3,
    }

    res = client.patch(detail_url(3), json=payload)
    data = res.get_json()

    assert res.status_code == 404
    assert data['error'] == 'Not Found'
    assert data['status'] == '404'
    assert data['method'] == 'PATCH'
    assert data['message'] == "A job doesn't exist."
    assert data['path'] == "/jobs/3"


def test_destroy_job_successfully(client):
    job_id = add_job(1, [2, 3], date(2021, 1, 1), time(11, 30), 2.0)

    res = client.delete(detail_url(job_id))
    data = res.get_json()

    assert res.status_code == 200
    assert data['id'] == job_id
    assert data['employee_ids'] == '2,3'
    assert data['date'] == '2021-01-01'
    assert data['start_time'] == '11:30:00'
    assert data['hours_number'] == 2.0


def test_destroy_job_that_not_exists_fails(client):
    res = client.delete(detail_url(3))
    data = res.get_json()

    assert res.status_code == 404
    assert data['error'] == 'Not Found'
    assert data['status'] == '404'
    assert data['method'] == 'DELETE'
    assert data['message'] == "A job doesn't exist."
    assert data['path'] == "/jobs/3"
