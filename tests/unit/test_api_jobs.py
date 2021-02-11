from datetime import time, date

from src.accounting import db
from src.accounting.models import Job

JOBS_URL = '/jobs'


def detail_url(job_id):
    return f'{JOBS_URL}/{job_id}'


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


def test_retrieve_a_single_job_successfully(client):
    job_id = add_job(1, [2, 3], date(2021, 1, 1), time(11, 30), 2.0)

    res = client.get(detail_url(job_id))
    data = res.get_json()

    assert res.status_code == 200
    assert data['id'] == job_id
    assert data['customer'] == 1
    assert data['employees'] == '2,3'
    assert data['date'] == '2021-01-01'
    assert data['start_time'] == '11:30:00'
    assert data['hours_number'] == 2.0


def test_retrieve_a_single_job_that_not_exists_fails(client):
    res = client.get(detail_url(2))

    assert res.status_code == 200
    assert b"A job doesn't exists" in res.data
