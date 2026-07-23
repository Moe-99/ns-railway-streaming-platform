import requests
from datetime import datetime

from app.config.settings import Settings
from app.models.departure_event import DepartureEvent


class NSClient:
    def __init__(self, settings: Settings):
        self.settings = settings

        self.headers = {
            "Ocp-Apim-Subscription-Key": settings.ns_api_key
        }

    def _send_request(self, station: str) -> dict:
        params = {
            "station": station
        }

        response = requests.get(
            self.settings.ns_api_url,
            headers=self.headers,
            params=params,
            timeout=self.settings.request_timeout,
        )

        response.raise_for_status()

        return response.json()

    def _create_departure(
        self,
        departure_data: dict,
        station: str,
    ) -> DepartureEvent:

        return DepartureEvent(
            station=station,
            destination=departure_data["direction"],
            planned_departure=datetime.fromisoformat(
                departure_data["plannedDateTime"]
            ),
            actual_departure=datetime.fromisoformat(
                departure_data["actualDateTime"]
            ),
            planned_track=departure_data["plannedTrack"],
            actual_track=departure_data["actualTrack"],
            cancelled=departure_data["cancelled"],
            status=departure_data["departureStatus"],
            train_type=departure_data["trainCategory"],
        )

    def _parse_departures(
        self,
        payload: dict,
        station: str,
    ) -> list[DepartureEvent]:

        departures = []

        for departure_data in payload["departures"]:
            event = self._create_departure(
                departure_data,
                station,
            )

            departures.append(event)

        return departures

    def fetch_departures(
        self,
        station: str,
    ) -> list[DepartureEvent]:

        payload = self._send_request(station)

        departures = self._parse_departures(
            payload,
            station,
        )

        return departures