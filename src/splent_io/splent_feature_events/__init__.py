from splent_framework.admin import register_admin_resource
from splent_framework.blueprints.base_blueprint import create_blueprint
from splent_framework.services.service_locator import register_service

from splent_io.splent_feature_events.models import Event
from splent_io.splent_feature_events.services import EventsService

events_bp = create_blueprint(__name__)


def init_feature(app):
    register_service(app, "EventsService", EventsService)

    # Surface Event in the admin panel (the wp-admin-style back-office).
    register_admin_resource(
        Event,
        name="event",
        label="Event",
        label_plural="Events",
        icon="calendar",
        group="Programme",
        order=10,
        list_columns=["title", "kind", "room", "starts_at"],
        field_widgets={
            "summary": "textarea",
            "description": "richtext",
            "image": "image",
            "link": "url",
            "kind": "select",
            "slug": "slug",
            "starts_at": "datetime",
            "ends_at": "datetime",
            "published": "bool",
        },
        feature="events",
    )


def inject_context_vars(app):
    return {}
