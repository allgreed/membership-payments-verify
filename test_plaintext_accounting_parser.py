from datetime import date
import plaintext_accounting_parser
from plaintext_accounting_parser import Transaction


def test_parse_single():
    single_transaction = """1987-05-06 food
    ble       13.00 XYZ
    fuj      -13.00 XYZ"""

    assert plaintext_accounting_parser.parse(single_transaction) == plaintext_accounting_parser.Transaction(title="food", date=date(year=1987, month=5, day=6))


def test_parse_many():
    single_transaction = """1987-01-06 food
    ble       13.00 XYZ
    fuj      -13.00 XYZ"""
    journal = f"""{single_transaction}

{single_transaction}"""
    reference_trn = plaintext_accounting_parser.parse(single_transaction)

    assert plaintext_accounting_parser.parse_many(journal) == [reference_trn, reference_trn]


def test_dont_crash_on_other_stuff():
    single_transaction = """1987-01-06 food
    ble       13.00 XYZ
    fuj      -13.00 XYZ"""
    reference_trn = plaintext_accounting_parser.parse(single_transaction)
    journal = f"""account assets      ; type:A, things I own

commodity $1000.00

{single_transaction}

D 1000.00 PLN

P 1967/12/14 Foo:Bar 1244 BLD
P 1235/03/34 Ble:Fuj 4552 SRA

"""
    assert plaintext_accounting_parser.parse_many(journal) == [reference_trn]
