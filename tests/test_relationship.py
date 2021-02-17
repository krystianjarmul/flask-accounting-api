from datetime import date, time

from src.accounting import db
from src.accounting.models import Job, Customer, Employee
from .helpers import add_job, add_customer, add_employee, assign_customer, \
    assign_employee


def test_assign_customer_to_job_provides_access_to_jobs_from_customer(session):
    customer_id = add_customer('Stefan Miller', 11.5)
    job_id = add_job(date(2021, 11, 11), time(11, 30), 2.0)
    job = Job.query.get(job_id)
    customer = Customer.query.get(customer_id)

    job.customer_id = customer_id
    session.add(job)
    session.commit()

    assert customer.jobs == [job]


def test_assign_employee_to_job_provides_access_to_jobs_from_employee(session):
    employee_id = add_employee('Anna Testowa')
    job_id = add_job(date(2021, 11, 11), time(11, 30), 2.0)
    job = Job.query.get(job_id)
    employee = Employee.query.get(employee_id)

    job.employees.append(employee)
    session.add(job)
    session.commit()

    assert employee.jobs == [job]


def test_delete_job_with_assigned_employee_not_remove_employee(session):
    employee_id = add_employee('Anna Testowa')
    job_id = add_job(date(2021, 1, 1), time(11, 30), 2.5)
    job, _ = assign_employee(job_id, employee_id)

    session.delete(job)
    session.commit()

    assert Job.query.get(job_id) is None
    assert Employee.query.get(employee_id)


def test_delete_job_with_assigned_customer_not_remove_customer(session):
    customer_id = add_customer('Stefan Miller', 12.0)
    job_id = add_job(date(2021, 1, 1), time(11, 30), 2.5)
    job, _ = assign_customer(job_id, customer_id)

    session.delete(job)
    session.commit()

    assert Job.query.get(job_id) is None
    assert Customer.query.get(customer_id)


def test_delete_employee_assigned_to_job_not_remove_the_job(session):
    employee_id = add_employee('Katarzyna Test')
    job_id = add_job(date(2011, 1, 1), time(10, 30), 2.5)
    _, employee = assign_employee(job_id, employee_id)

    session.delete(employee)
    session.commit()

    assert Employee.query.get(employee_id) is None
    assert Job.query.get(job_id)


def test_delete_customer_assigned_to_job_not_remove_the_job(session):
    customer_id = add_customer('Michael Jordan', 13.0)
    job_id = add_job(date(2021, 2, 1), time(10, 30), 2.5)
    _, customer = assign_customer(job_id, customer_id)

    session.delete(customer)
    session.commit()

    assert Customer.query.get(customer_id) is None
    assert Job.query.get(job_id)
