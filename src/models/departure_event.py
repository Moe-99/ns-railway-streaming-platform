from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class DepartureEvent:
    station: str
    destination: str
    planned_departure: datetime
    actual_departure: datetime | None
    planned_track: str | None
    actual_track: str | None
    cancelled: bool
    status: str
    train_type: str

