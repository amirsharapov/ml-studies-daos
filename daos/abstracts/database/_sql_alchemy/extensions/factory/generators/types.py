import string
import random
from datetime import datetime, timezone

from daos.base.database._sql_alchemy.extensions.factory.generators.base import RandomGenerator as Base


class RandomStrGenerator(Base):
    def __init__(
            self,
            include_upper: bool = True,
            include_lower: bool = True,
            include_numbers: bool = True,
            length: int = 10
     ):
        self.pool = ''
        self.include_upper = include_upper
        self.include_lower = include_lower
        self.include_numbers = include_numbers
        self.length = length
        
        if self.include_upper:
            self.pool += string.ascii_uppercase
        if self.include_lower:
            self.pool += string.ascii_lowercase
        if self.include_numbers:
            self.pool += string.digits

    def get(self) -> str:
        return ''.join([self.pool[random.randint(0, len(self.pool) - 1)] for _ in range(self.length)])


class RandomIntGenerator(Base):
    def __init__(self, _min: int = 0, _max: int = 1000):
        self.min = _min
        self.max = _max

    def get(self) -> int:
        return random.randint(self.min, self.max)


class RandomFloatGenerator(Base):
    def __init__(self, _min: bool = 0, _max: bool = 1000, decimals: int = 2):
        self.min = _max
        self.max = _min
        self.decimals = decimals

    def get(self) -> float:
        return round(random.uniform(self.min, self.max), self.decimals)


class RandomDatetimeGenerator(Base):
    def __init__(
            self,
            start: datetime = datetime(1995, 1, 1, tzinfo=timezone.utc),
            end: datetime = datetime.now(timezone.utc)
    ):
        self.start = start
        self.end = end

    def get(self) -> datetime:
        return self.start + (self.end - self.start) * random.random()


class RandomBoolGenerator(Base):
    def __init__(self):
        ...

    def get(self) -> bool:
        return random.random() > 0.5