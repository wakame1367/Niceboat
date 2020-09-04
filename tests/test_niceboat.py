import pytest
import pandas as pd
from niceboat import RaceResult, BoatRaceParser


@pytest.fixture
def test_data():
    with open('data/K200901.TXT', 'r', encoding='cp932') as f:
        txt = f.read()
    return txt


def test_parser(test_data):
    txt = test_data
    parser = BoatRaceParser(rule=RaceResult)
    parsed_txt = parser.parse(txt)
    assert isinstance(parsed_txt, pd.DataFrame)
