from pathlib import Path

import pandas as pd
import pytest

from niceboat import RaceResult, BoatRaceParser

test_data_path = Path('tests/data/')


@pytest.fixture
def normal_case():
    return open_txt_file(test_data_path / 'K200901.TXT')


@pytest.fixture()
def exception_case():
    return open_txt_file(test_data_path / 'ex_K200901.TXT')


def open_txt_file(path):
    with open(path, 'r', encoding='cp932') as f:
        txt = f.read()
    return txt


def test_parser(normal_case):
    txt = normal_case
    parser = BoatRaceParser(rule=RaceResult)
    parsed_txt = parser.parse(txt)
    assert isinstance(parsed_txt, pd.DataFrame)


def test_parser_exception_pattern(exception_case):
    txt = exception_case
    parser = BoatRaceParser(rule=RaceResult)
    parsed_txt = parser.parse(txt)
    assert isinstance(parsed_txt, pd.DataFrame)
