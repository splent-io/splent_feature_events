from datetime import datetime  # noqa: F401 — used by seeders/migrations

from splent_framework.db import db


class Event(db.Model):
    """An event/activity: a talk, workshop, competition or ceremony."""

    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True, index=True)
    kind = db.Column(db.String(64), default="talk")  # talk|workshop|competition|ceremony
    summary = db.Column(db.Text, default="")
    description = db.Column(db.Text, default="")      # rich text / HTML
    speaker = db.Column(db.String(255), default="")
    room = db.Column(db.String(128), default="")
    starts_at = db.Column(db.DateTime)
    ends_at = db.Column(db.DateTime)
    image = db.Column(db.String(512), default="")
    link = db.Column(db.String(512), default="")
    published = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"Event<{self.slug}>"
