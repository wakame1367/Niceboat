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
        self.header = ["landing_boat", "reg_number", "player_name",
                       "mortar", "board", "exhibition",
                       "approach", "start_timing", "race_time"]

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
                    player = player.lstrip()
                    # http://boat-advisor.com/soft/manual/data_keyword.htm
                    # https://github.com/wakamezake/boatrace/issues/1
                    arrival_key = player[0].upper()
                    split_values = player.split(maxsplit=len(self.header))
                    # Late start
                    if arrival_key == 'L':
                        # ex. L0  3 4262 馬場貴也　 38   19  6.53       L .        .  .
                        # ex. L0  1 2841 吉田稔　 57   30  6.78   1   L1.99      .  .
                        approach = split_values[7]
                        if approach == 'L':
                            split_values = split_values[:7] + [None] * 3
                        else:
                            split_values[8] = split_values[8].lstrip('L')
                            split_values = split_values[:9] + [None]
                    # Flying Start
                    elif arrival_key == 'F':
                        # ex. F   1 4069 山本修一　 42   54  6.55   1   F0.01      .  .
                        split_values[8] = split_values[8].lstrip('F')
                    # Absence
                    elif arrival_key == 'K':
                        # ex. K0  1 3957 大谷直弘 23   36 K .         K .        .  .
                        split_values = split_values[:6]
                        split_values += [None] * 4

                    race_time = split_values[-1]
                    if race_time == '.  . ':
                        split_values[-1] = None
                    # skip index
                    lines.append(split_values[1:])
        return pd.DataFrame(lines, columns=self.header)

    def _preprocess(self, txt):
        txt = txt.replace('\u3000', '')
        return txt
