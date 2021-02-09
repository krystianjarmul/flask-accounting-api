from app import app

EMPLOYEE_URL = '/employees/'

client = app.test_client()


def test_retrieve_list_of_employees():
    res = client.get(EMPLOYEE_URL)

    assert res.status_code == 200
