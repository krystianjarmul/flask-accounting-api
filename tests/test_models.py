from datetime import date, time
from src.accounting.models import Job, Employee


def test_end_time():
    job1 = Job(date(2021, 1, 2), time(11, 30), 2)
    job2 = Job(date(2021, 1, 2), time(15, 0), 2.5)
    job3 = Job(date(2021, 1, 2), time(7, 0), 1)
    assert job1.end_time == time(13, 30)
    assert job2.end_time == time(17, 30)
    assert job3.end_time == time(8, 0)


def test_hours_per_employee():
    job = Job(date(2021, 1, 2), time(11, 30), 6)
    employee1 = Employee('Anna Testowa')
    employee2 = Employee('Maria Test')
    job.employees.append(employee1)
    job.employees.append(employee2)
    assert job.hours_per_employee == 3.0