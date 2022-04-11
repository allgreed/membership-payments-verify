import yaml
import calendar
from dataclasses import dataclass
from typing import Callable, List, Tuple
from datetime import date, datetime

import plaintext_accounting_parser


# TODO: come up with a better name than Ble
@dataclass
class Ble:
    customer: str
    start: date
    end: date
    service: str


def main():
    with open("example.yaml") as f:
        config = yaml.load(f.read(), Loader=yaml.SafeLoader) 

    # TODO: check if intervals are implemented

    for s in config["services"]:
        interval = config["services"][s]["interval"]
        if interval not in config["intervals"]:
            raise ValueError(f"interval \"{interval}\" for service \"{s['name']}\" not supported")

    for c in config["customers"]:
        s = c["service"]
        if s not in map(lambda x: x, config["services"]):
            raise ValueError(f"service \"{s}\" for customer \"{c['name']}\" not supported")

    entries = generate_entries(config, now_fn=now)

    from pprint import pprint
    pprint(entries)
    # !!! TODO !!! <- implement this for MVP
    # read transactions
    # parse transations
    # parametrize where config file is acquired from
    # parametrize where transaction file is acquired from

    # match payments with Bles
    # find unmatches == overdue
    # display

    # TODO: add and verify price


def generate_entries(config: dict, now_fn: Callable[[], date]) -> List[Ble]:
    now = now_fn()

    result = []
    for c in config["customers"]:
        name, service, _start, _end = c["name"], c["service"], c["start"], c["end"]
        start = datetime.strptime(_start, "%d-%M-%Y").date()
        end = datetime.strptime(_end, "%d-%M-%Y").date() if _end is not None else None
        interval = config["services"][service]["interval"]

        for start_end in compute_wall_intervals(start, end, interval, now):
            result.append(Ble(customer=name, service=service, start=start_end[0], end=start_end[1]))

    return result


def compute_wall_intervals(start: date, end: date, interval: str, now: date) -> List[Tuple[date, date]]:
    end = end or now
    definite_end = min(now, end)
    result = []

    if interval != "monthly":
        raise NotImplementedError(f"interval {interval} is not supported")
    assert interval == "monthly", "please add actual dispatch logic and startup checks when implementing other intervals"

    i = start
    while i < definite_end: # TODO: how about <= ?
        result.append((i, date(i.year, i.month, calendar.monthrange(i.year, i.month)[1])))
        i = date(i.year, i.month + 1, i.day)

    # TODO: verify intervals overlapping

    return result


def now() -> date:
    return datetime.now().date()


if __name__ == "__main__":
    main()
