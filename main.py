import yaml
import os
import re
import calendar
from dataclasses import dataclass
from typing import Callable, List, Tuple
from datetime import date, datetime

import plaintext_accounting_parser


@dataclass
class Obligation:
    customer: str
    start: date
    end: date
    service: str

@dataclass
class Payment:
    customer: str
    start: date
    end: date
    service: str


def main():
    with open(os.environ.get("APP_MEMBERSHIP_CONFIG", os.path.expanduser("~/Documents/finance/membership.yaml")), "r") as f:
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

    obligations = generate_obligations(config, now_fn=now)

    with open(os.environ["LEDGER_FILE"], "r") as f:
        transactions = plaintext_accounting_parser.parse_many(f.read())
    
    customer_transactions = filter(lambda t: t.title.startswith("Payment for"), transactions)
    _payments = map(parse_customer_transaction, customer_transactions)
    payments = list(_payments)

    for p in payments:
        r = set()
        for i, o in enumerate(obligations):
            if matches(p, o):
                r.add(i)

        if not r:
            raise RuntimeError(f"Unmatched payment {p}")

        for i in sorted(r, reverse=True):
            del obligations[i]

    from pprint import pprint
    pprint(obligations)

    # TODO: add a period to pay backwards
    # TODO: add and verify price


def matches(p, o) -> bool:
    if o.customer == p.customer and p.service == o.service:
        # TODO: assert interval for service is "monthly"
        result = p.start <= o.start and p.end >= o.end
        return result

    return False


def parse_customer_transaction(t: plaintext_accounting_parser.Transaction) -> Payment:
    m = re.match(r"Payment for (\w+) \[(.\w+\s?\w*)\] (.*)", t.title)
    service, customer, period = m.groups()

    start = t.date

    if period == "for current month":
        start = date(year=t.date.year, month=t.date.month, day=1)
        end = date(year=t.date.year, month=t.date.month, day=calendar.monthrange(t.date.year, t.date.month)[1])
    elif period.startswith("until"):
        _, d = period.split(" ")

        try:
            end = datetime.strptime(d, "%d/%m/%Y").date()
        except ValueError:
            print(d)
            raise
    else:
        raise NotImplementedError(f"period \"{period}\" not supported")

    return Payment(service=service, customer=customer, start=start, end=end)


def generate_obligations(config: dict, now_fn: Callable[[], date]) -> List[Obligation]:
    now = now_fn()

    result = []
    for c in config["customers"]:
        name, service, _start, _end = c["name"], c["service"], c["start"], c["end"]
        start = datetime.strptime(_start, "%d-%M-%Y").date()
        end = datetime.strptime(_end, "%d-%M-%Y").date() if _end is not None else None
        interval = config["services"][service]["interval"]

        for start_end in compute_wall_intervals(start, end, interval, now):
            result.append(Obligation(customer=name, service=service, start=start_end[0], end=start_end[1]))

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
