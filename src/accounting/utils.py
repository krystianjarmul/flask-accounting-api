from typing import Any


def update_model(instance: Any, data: dict):
    for attr in instance.__dict__.keys():
        if attr not in data:
            continue
        setattr(instance, attr, data.get(attr))