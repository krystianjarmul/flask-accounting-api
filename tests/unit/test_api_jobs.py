from datetime import time, date

from src.accounting import db
from src.accounting.models import Job

JOBS_URL = '/jobs'


def add_job(cid, eids, d, st, hn):
    job = Job(cid, eids, d, st, hn)
    db.session.add(job)
    db.session.commit()
    return job.id


def test_retrieve_list_of_jobs(client):
    add_job(1, [2, 3], date(2021, 1, 1), time(11, 30), 2.0)
    add_job(2, [1], date(2021, 2, 1), time(10, 30), 2.5)
    add_job(3, [4, 5], date(2021, 1, 3), time(11, 00), 1.0)

    res = client.get(JOBS_URL)
    data = res.get_json()

    assert res.status_code == 200
    assert len(data) == 3

