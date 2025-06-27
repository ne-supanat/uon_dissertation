import enum
from pydantic import BaseModel


class InputOutput(BaseModel):
    input: str
    output: str


class Archetype(enum.Enum):
    PragmaticCommuter = "Pragmatic Commuter"
    EnvironmentallyAwareCommuter = "Environmentally Aware Commuter"


class Profile(BaseModel):
    file: str
    attrs: list[str]
    quotes: list[str]
    archetype: Archetype


class TransportationMode(enum.Enum):
    Tram = "Tram"
    Cycling = "Cycling"
    Bus = "Bus"
    Driving = "Driving"
