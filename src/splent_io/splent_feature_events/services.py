from splent_io.splent_feature_events.repositories import EventsRepository
from splent_framework.services.BaseService import BaseService


class EventsService(BaseService):
    def __init__(self):
        super().__init__(EventsRepository())

    def list_published(self):
        return self.repository.list_published()

    def get_by_slug(self, slug: str):
        return self.repository.get_by_slug(slug)
