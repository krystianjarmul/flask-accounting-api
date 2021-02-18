from datetime import date, time
from typing import Tuple

from src.accountment import db
from src.accountment.models import Job, Customer, Employee


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


def assign_customer(jid: int, cid: int) -> Tuple[Job, Customer]:
    job = Job.query.get(jid)
    customer = Customer.query.get(cid)
    job.customer_id = cid
    db.session.commit()
    return job, customer


def assign_employee(jid: int, eid: int) -> Tuple[Job, Employee]:
    job = Job.query.get(jid)
    employee = Employee.query.get(eid)
    job.employees.append(employee)
    db.session.commit()
    return job, employee
