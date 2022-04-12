from typing import List
from datetime import date, datetime
from dataclasses import dataclass

@dataclass
class Transaction():
    title: str
    date: date
    # TODO: write rest of this stuff


def parse(raw_transaction: str) -> Transaction:
    first, *rest = raw_transaction.split("\n")
    # because title may contain spaces
    raw_date, *_title = first.split(" ")
    title = " ".join(_title)
    _date = datetime.strptime(raw_date, "%Y-%M-%d").date()
    return Transaction(title=title, date=_date)


def parse_many(journal: str) -> List[Transaction]:
    jounrnal_lines = journal.split("\n")
    
    result = []
    acc = []

    is_in_transaction = [False]
    for l in jounrnal_lines:
        # print(l, "a")
        
        if not is_in_transaction[0] and l != "" and l[0].isdigit():
            is_in_transaction[0] = True

        if is_in_transaction[0]:
            # print("in trn")
            if l == "":
                result.append(parse("\n".join(acc)))
                acc.clear()
                # print("zoink")
                is_in_transaction[0] = False
            else:
                acc.append(l)
    if acc:
        result.append(parse("\n".join(acc)))

    return result
