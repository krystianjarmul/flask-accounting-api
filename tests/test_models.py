from datetime import date, time
from src.accounting.models import Job


def test_job_calculates_end_time():
    job1 = Job(date(2021, 1, 2), time(11, 30), 2)
    job2 = Job(date(2021, 1, 2), time(15, 0), 2.5)
    job3 = Job(date(2021, 1, 2), time(7, 0), 1)
    assert job1.end_time == time(13, 30)
    assert job2.end_time == time(17, 30)
    assert job3.end_time == time(8, 0)
