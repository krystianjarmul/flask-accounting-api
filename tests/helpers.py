from datetime import date, time

from src.accounting import db
from src.accounting.models import Job, Customer, Employee


def add_job(d: date, st: time, hn: float) -> int:
    job = Job(d, st, hn)
    db.session.add(job)
    db.session.commit()
    return job.id


def add_customer(name: str, hr: float) -> int:
    customer = Customer(name, hr)
    db.session.add(customer)
    db.session.commit()
    return customer.id


def add_employee(name: str) -> int:
    employee = Employee(name)
    db.session.add(employee)
    db.session.commit()
    return employee.id
