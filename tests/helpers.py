from src.accounting import db
from src.accounting.models import Job, Customer, Employee


def add_job(cid, eids, d, st, hn):
    job = Job(cid, eids, d, st, hn)
    db.session.add(job)
    db.session.commit()
    return job.id


def add_customer(name, hr):
    customer = Customer(name, hr)
    db.session.add(customer)
    db.session.commit()
    return customer.id


def add_employee(name):
    employee = Employee(name)
    db.session.add(employee)
    db.session.commit()
    return employee.id
