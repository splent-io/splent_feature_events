from __future__ import annotations

from splent_io.splent_feature_events.models import Event
from splent_framework.repositories.BaseRepository import BaseRepository


class EventsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Event)

    def list_published(self) -> list[Event]:
        return (
            Event.query.filter_by(published=True)
            .order_by(Event.order.asc(), Event.starts_at.asc())
            .all()
        )

    def get_by_slug(self, slug: str) -> Event | None:
        return Event.query.filter_by(slug=slug).first()
