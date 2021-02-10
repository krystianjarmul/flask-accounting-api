from src.accounting import db
from src.accounting.models import Customer

CUSTOMER_URL = '/customers'


def detail_url(customer_id):
    return f'{CUSTOMER_URL}/{customer_id}'


def add_customer(name, hr):
    customer = Customer(name, hr)
    db.session.add(customer)
    db.session.commit()
    return customer.id


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

    assert res.status_code == 404
    assert b"A customer doesn't exist" in res.data


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


def test_create_a_customer_with_invalid_payload_fails(client):
    payload = {
        'name': '',
        'hourly_rate': '',
    }

    res = client.post(CUSTOMER_URL, json=payload)

    assert res.status_code == 400
    assert b'Not a valid number' in res.data


def