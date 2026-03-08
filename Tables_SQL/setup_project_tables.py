from create_events_table import main as setup_events
from create_users_table import main as setup_users
from create_persons_table import main as setup_persons
from create_event_attendees_table import main as setup_event_attendees


def main() -> None:
    setup_users()
    setup_events()
    setup_persons()
    setup_event_attendees()
    print("Project tables are ready.")


if __name__ == "__main__":
    main()
