import datetime # Aggiungi questo import in alto!
from dataclasses import dataclass

@dataclass
class Sighting:
    id: int
    datetime: datetime.datetime
    city: str
    state: str
    country: str
    shape: str
    duration: int
    duration_hm: str
    comments: str
    date_posted: datetime.datetime
    latitude: float
    longitude: float

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"{self.city} ({self.state}) - {self.datetime} - {self.duration_hm}"