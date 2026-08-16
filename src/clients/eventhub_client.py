from dataclasses import asdict
import json
from src.models.departure_event import DepartureEvent
from azure.eventhub import EventData, EventHubProducerClient
from src.config.settings import Settings


class EventHubClient:

    def __init__(self, settings:Settings):
        self.settings = settings

        self.producer = EventHubProducerClient.from_connection_string(
            conn_str=settings.eventhub_connection_string,
            eventhub_name=settings.eventhub_name,
            retry_total=settings.retry_total,
            retry_backoff_factor=settings.retry_backoff_factor,
            retry_mode=settings.retry_mode
        )


    def _serialize_event(self, departure: DepartureEvent) -> str:
        data = asdict(departure)
        data["planned_departure"] = data["planned_departure"].isoformat()
        data["actual_departure"] = data["actual_departure"].isoformat()

        json_data = json.dumps(data)
        return json_data

    def send(self, departures: list[DepartureEvent]):

        if not departures:
            return

        batch = self.producer.create_batch()

        for departure in departures:

            json_data = self._serialize_event(departure)

            event = EventData(json_data)

            try:
                batch.add(event)
            except ValueError:
                self.producer.send_batch(batch)
                batch = self.producer.create_batch()
                try:
                    batch.add(event)
                except ValueError:
                    raise ValueError(
                    "Event is too large to fit in an empty Event Hub batch.")

        self.producer.send_batch(batch)


           

             

