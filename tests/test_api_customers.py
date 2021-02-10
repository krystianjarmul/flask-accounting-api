from src.accounting import db
from src.accounting.models import Customer

CUSTOMER_URL = '/customers'


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


