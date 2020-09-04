"""Awesome package."""
import logging
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

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
        self.race_end: str = self.name + self.race_end_suffix


RaceResult = Base(name='K')
RaceCard = Base(name='B')


class BaseParser(metaclass=ABCMeta):
    @abstractmethod
    def parse(self):
        pass
