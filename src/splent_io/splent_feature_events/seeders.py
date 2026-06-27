from datetime import datetime

from splent_framework.seeders.BaseSeeder import BaseSeeder

from splent_io.splent_feature_events.models import Event


class EventsSeeder(BaseSeeder):
    def run(self):
        self.seed(
            [
                Event(
                    slug="opening-ceremony", title="Opening Ceremony", kind="ceremony",
                    room="Salón de Actos", order=1, starts_at=datetime(2025, 11, 4, 9, 0),
                    summary="Kick-off of InnoSoft Days XIII at the ETSII.",
                    description="<p>Welcome to three days of talks, workshops, "
                                "competitions and fun.</p>",
                ),
                Event(
                    slug="ai-testing", title="New Ways to Test Software using AI", kind="talk",
                    room="Aula 0.1", order=2, starts_at=datetime(2025, 11, 4, 10, 0),
                    speaker="Andreas Zeller", link="https://andreas-zeller.info",
                    summary="Keynote on AI-assisted software testing.",
                    description="<p>How AI is changing the way we test software.</p>",
                ),
                Event(
                    slug="escape-room-grace", title="Escape Room — Grace's Enigma",
                    kind="competition", room="Lab 2", order=3,
                    starts_at=datetime(2025, 11, 5, 16, 0),
                    summary="A software-themed escape room.",
                ),
                Event(
                    slug="closing-ceremony", title="Closing Ceremony", kind="ceremony",
                    room="Salón de Actos", order=99, starts_at=datetime(2025, 11, 6, 18, 0),
                    summary="Awards and farewell.",
                ),
            ]
        )
