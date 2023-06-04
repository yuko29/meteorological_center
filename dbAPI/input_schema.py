from typing import TypedDict
from strongtyping.strong_typing import match_class_typing
from datetime import datetime

@match_class_typing
class NecessaryEarthquakeType(TypedDict):
    time: datetime
    factory: str
    magnitude: float


@match_class_typing
class NecessaryElectricityType(TypedDict):
    time: datetime
    region: str
    power_usage: float
    power_generate: float


@match_class_typing
class NecessaryReservoirType(TypedDict):
    time: datetime
    name: str
    percentage: float