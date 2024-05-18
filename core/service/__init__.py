from itertools import count, takewhile
from typing import Iterator

from core.service.anchor import Anchor
from core.service.color import Color
from core.service.event_type import EventType


def float_range(start: float, stop: float, step: float) -> Iterator[float]:
    return takewhile(lambda x: x < stop, count(start, step))
