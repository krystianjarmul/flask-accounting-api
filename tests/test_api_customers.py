from src.accounting import db
from src.accounting.models import Customer
from tests.helpers import add_customer

CUSTOMER_URL = '/customers'


def detail_url(customer_id):
    return f'{CUSTOMER_URL}/{customer_id}'


def test_retrieve_a_list_of_customers(client):
    add_customer('Steven Hawkins', 13.5)
    add_customer('Michael Ballack', 12.5)
    add_customer('Albert Einstein', 11.0)

    res = client.get(CUSTOMER_URL)
    data = res.get_json()

    assert res.status_code == 200
    assert len(data) == 3


def test_retrieve_a_single_customer_successfully(client):
    customer_id = add_customer('Steven Hawkins', 13.0)

    res = client.get(detail_url(customer_id))
    data = res.get_json()

    assert res.status_code == 200
    assert data['id'] == customer_id
    assert data['name'] == 'Steven Hawkins'
    assert data['hourly_rate'] == 13.0


def test_retrieve_a_single_customer_that_not_exists_fails(client):
    res = client.get(detail_url(5))
    data = res.get_json()

    assert res.status_code == 404
    assert data['error'] == 'Not Found'
    assert data['status'] == '404'
    assert data['method'] == 'GET'
    assert data['message'] == "A customer doesn't exist."
    assert data['path'] == "/customers/5"


def test_create_a_customer_successfully(client):
    payload = {
        'name': 'Steven Hawkins',
        'hourly_rate': 12.5,
    }

    res = client.post(CUSTOMER_URL, json=payload)
    data = res.get_json()

    assert res.status_code == 201
    assert data['id'] == 1
    assert data['name'] == payload['name']
    assert data['hourly_rate'] == payload['hourly_rate']


def test_create_a_customer_with_empty_payload_fails(client):
    payload = {}

    res = client.post(CUSTOMER_URL, json=payload)
    data = res.get_json()

    assert res.status_code == 400
    assert data['error'] == 'Bad Request'
    assert data['status'] == '400'
    assert data['method'] == 'POST'
    assert data['messages'] == {
        'name': ['Missing data for required field.'],
        'hourly_rate': ['Missing data for required field.']
    }
    assert data['path'] == '/customers'


def test_create_a_customer_with_invalid_payload_fails(client):
    payload = {
        'name': 'Stefan Miller',
        'hourly_rate': '',
    }

    res = client.post(CUSTOMER_URL, json=payload)
    data = res.get_json()

    assert res.status_code == 400
    assert data['error'] == 'Bad Request'
    assert data['status'] == '400'
    assert data['method'] == 'POST'
    assert data['messages'] == {'hourly_rate': ['Not a valid number.']}
    assert data['path'] == '/customers'


def test_partial_update_a_customer_successfully(client):
    customer_id = add_customer('Steven Hawking', 11.5)
    payload = {
        'hourly_rate': 12.0
    }

    res = client.patch(detail_url(customer_id), json=payload)
    data = res.get_json()

    assert res.status_code == 200
    assert data['id'] == customer_id
    assert data['name'] == 'Steven Hawking'
    assert data['hourly_rate'] == 12.0


def test_partial_update_a_customer_that_not_exists_fails(client):
    payload = {
        'hourly_rate': 12.0
    }

    res = client.patch(detail_url(4), json=payload)
    data = res.get_json()

    assert res.status_code == 404
    assert data['error'] == 'Not Found'
    assert data['status'] == '404'
    assert data['method'] == 'PATCH'
    assert data['message'] == "A customer doesn't exist."
    assert data['path'] == "/customers/4"


def test_partial_update_a_customer_with_invalid_payload_fails(client):
    customer_id = add_customer('Steven Hawking', 11.50)
    payload = {
        'hourly_rate': -3
    }

    res = client.patch(detail_url(customer_id), json=payload)
    data = res.get_json()

    assert res.status_code == 400
    assert data['error'] == 'Bad Request'
    assert data['status'] == '400'
    assert data['method'] == 'PATCH'
    assert data['messages'] == {'hourly_rate': ['Not a positive number.']}
    assert data['path'] == '/customers/1'


def test_update_a_customer_successfully(client):
    customer_id = add_customer('Steven Hawking', 11.50)
    payload = {
        'name': 'Steven Hawkins',
        'hourly_rate': 13.0,
    }

    res = client.put(detail_url(customer_id), json=payload)
    data = res.get_json()

    assert res.status_code == 200
    assert data['id'] == customer_id
    assert data['hourly_rate'] == 13.0


def test_update_a_customer_with_incomplete_payload_fails(client):
    customer_id = add_customer('Steven Hawking', 11.50)
    payload = {
        'hourly_rate': 12,
    }

    res = client.put(detail_url(customer_id), json=payload)
    data = res.get_json()

    assert res.status_code == 400
    assert data['error'] == 'Bad Request'
    assert data['status'] == '400'
    assert data['method'] == 'PUT'
    assert data['messages'] == {'name': ['Missing data for required field.']}
    assert data['path'] == '/customers/1'


def test_delete_a_customer_successfully(client):
    customer_id = add_customer('Steven Hawking', 11.50)

    res = client.delete(detail_url(customer_id))
    data = res.get_json()

    assert res.status_code == 200
    assert data['id'] == customer_id
    assert data['name'] == 'Steven Hawking'
    assert data['hourly_rate'] == 11.50


def test_delete_a_customer_that_not_exists_fails(client):
    res = client.delete(detail_url(3))
    data = res.get_json()

    assert res.status_code == 404
    assert data['error'] == 'Not Found'
    assert data['status'] == '404'
    assert data['method'] == 'DELETE'
    assert data['message'] == "A customer doesn't exist."
    assert data['path'] == "/customers/3"
