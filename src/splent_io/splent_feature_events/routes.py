from flask import abort, render_template

from splent_io.splent_feature_events import events_bp
from splent_framework.services.service_locator import service_proxy

events_service = service_proxy("EventsService")


@events_bp.route("/events", methods=["GET"])
def index():
    events = events_service.list_published()
    return render_template("events/list.html", events=events)


@events_bp.route("/events/<slug>", methods=["GET"])
def detail(slug):
    event = events_service.get_by_slug(slug)
    if event is None:
        abort(404)
    return render_template("events/detail.html", event=event)
