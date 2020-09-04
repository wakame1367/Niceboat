"""Awesome package."""
import logging
import re
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

import pandas as pd
from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution

try:
    distribution = get_distribution(__name__)
    __version__ = distribution.version
except DistributionNotFound:
    pass

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()

logger.addHandler(handler)

logger.setLevel(logging.INFO)


@dataclass
class Base:
    name: str
    file_begin_prefix: str = 'START'
    file_end_prefix: str = 'FINAL'
    race_begin_suffix: str = 'BGN'
    race_end_suffix: str = 'END'
    sep_size: int = 79
    separator: str = "-" * sep_size
    players: int = 6

    def __post_init__(self):
        self.file_begin: str = self.file_begin_prefix + self.name
        self.file_end: str = self.file_end_prefix + self.name
        self.race_begin: str = self.name + self.race_begin_suffix
        self.race_begin_pat = re.compile(r'\d+{}'.format(self.race_begin))
        self.race_end: str = self.name + self.race_end_suffix
        self.race_end_pat = re.compile(r'\d+{}'.format(self.race_end))


RaceResult = Base(name='K')
RaceCard = Base(name='B')


class BaseParser(metaclass=ABCMeta):
    @abstractmethod
    def parse(self, txt):
        pass


class BoatRaceParser(BaseParser):
    def __init__(self, rule: Base):
        self.rule = rule

    def parse(self, txt) -> pd.DataFrame:
        txt = self._preprocess(txt)
        # Ignore the first separator
        # split per boat racing track
        lines = []
        lines_per_track = self.rule.race_begin_pat.split(txt)[1:]
        for line_per_track in lines_per_track:
            # per race
            line_per_race = line_per_track.split(self.rule.separator)
            header = line_per_race[0]
            for players_per_round in line_per_race[1:]:
                players_per_race = players_per_round.split('\n')[1:self.rule.players + 1]
                for player in players_per_race:
                    lines.append(player.split())
        return pd.DataFrame(lines)

    def _preprocess(self, txt):
        txt = txt.replace('\u3000', '')
        return txt
