import json

from app import app, Employee, db

EMPLOYEE_URL = '/employees/'

app.config.from_object('config.TestingConfig')
client = app.test_client()
db.create_all()


def test_retrieve_list_of_employees():
    employee = Employee('Alina Testowska')
    db.session.add(employee)
    db.session.commit()

    print(app.config['ENV'])

    res = client.get(EMPLOYEE_URL)
    data = res.get_json()

    assert res.status_code == 200
    assert data[0]['name'] == employee.name



