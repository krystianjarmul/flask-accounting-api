from datetime import date, time
from typing import Union

from src.accounting.models import Employee, Customer, Job


def update_person(person: Union[Employee, Customer], data: dict):
    for attr in person.__dict__.keys():
        if attr not in data:
            continue
        setattr(person, attr, data.get(attr))


def update_the_job(job: Job, data: dict):
    for attr in job.__dict__.keys():
        if attr not in data:
            continue

        if attr == 'date':
            setattr(job, attr, date.fromisoformat(data['date']))
        elif attr == 'start_time':
            setattr(job, attr, time.fromisoformat(data['start_time']))
        else:
            setattr(job, attr, data.get(attr))
