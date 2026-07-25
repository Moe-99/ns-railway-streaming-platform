from src.config.settings import Settings
from src.clients.ns_client import NSClient

def main():

    settings = Settings()
    client = NSClient(settings)

    departures = client.fetch_departures("UT")

    for departure in departures:
        print(
            f"{departure.station:<3} | "
            f"{departure.planned_departure:%H:%M} | "
            f"{departure.actual_departure:%H:%M} | "
            f"{departure.destination:<22} | "
            f"{departure.train_type:<3} | "
            f"P:{departure.planned_track:<2} | "
            f"A:{departure.actual_track:<2} | "
            f"Cancelled: {departure.cancelled:<5} | "
            f"{departure.status}"
    )

if __name__ == "__main__":
    main()