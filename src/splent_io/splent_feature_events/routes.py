import re

from flask import (
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required

from splent_io.splent_feature_events import events_bp
from splent_io.splent_feature_events.models import Event
from splent_framework.db import db
from splent_framework.services.service_locator import service_proxy

events_service = service_proxy("EventsService")


# =====================================================================
# PUBLIC
# =====================================================================
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


# =====================================================================
# ADMIN — domain-specific management (the "plugin" screen)
# =====================================================================
# Known kinds shown first in the grouped list and offered in the form.
KNOWN_KINDS = ["talk", "workshop", "competition", "ceremony"]


def _slugify(value):
    base = re.sub(r"[^a-z0-9]+", "-", (value or "").lower()).strip("-")
    return base or "event"


def _unique_slug(title, exclude_id=None):
    base = _slugify(title)
    slug, i = base, 2
    while True:
        q = Event.query.filter_by(slug=slug)
        if exclude_id:
            q = q.filter(Event.id != exclude_id)
        if not q.first():
            return slug
        slug, i = f"{base}-{i}", i + 1


def _ordered_groups():
    """All events (incl. drafts) grouped by kind; known kinds first, extras after."""
    grouped = {}
    for e in Event.query.order_by(
        Event.order.asc(), Event.starts_at.asc(), Event.title.asc()
    ).all():
        grouped.setdefault(e.kind or "talk", []).append(e)
    ordered = {g: grouped.pop(g) for g in KNOWN_KINDS if g in grouped}
    ordered.update(grouped)
    return ordered


def _known_groups():
    existing = [
        g[0] for g in db.session.query(Event.kind).distinct().all() if g[0]
    ]
    seen, out = set(), []
    for g in KNOWN_KINDS + existing:
        if g and g not in seen:
            seen.add(g)
            out.append(g)
    return out


def _form_to_data(form):
    return {
        "title": (form.get("title") or "").strip(),
        "kind": (form.get("kind") or "talk").strip() or "talk",
        "summary": (form.get("summary") or "").strip(),
        "description": (form.get("description") or "").strip(),
        "speaker": (form.get("speaker") or "").strip(),
        "room": (form.get("room") or "").strip(),
        "starts_at": _parse_dt(form.get("starts_at")),
        "ends_at": _parse_dt(form.get("ends_at")),
        "image": (form.get("image") or "").strip(),
        "link": (form.get("link") or "").strip(),
        "order": int(form.get("order") or 0),
        "published": bool(form.get("published")),
    }


def _parse_dt(value):
    value = (value or "").strip()
    if not value:
        return None
    from datetime import datetime

    for fmt in ("%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


@events_bp.route("/admin/events", methods=["GET"])
@login_required
def admin_index():
    return render_template(
        "events/admin/list.html",
        groups=_ordered_groups(),
        known_groups=_known_groups(),
    )


@events_bp.route("/admin/events/new", methods=["GET", "POST"])
@login_required
def admin_new():
    if request.method == "POST":
        data = _form_to_data(request.form)
        if not data["title"]:
            flash("Title is required.", "danger")
            return redirect(url_for("events.admin_new"))
        data["slug"] = _unique_slug(data["title"])
        db.session.add(Event(**data))
        db.session.commit()
        flash(f"Added {data['title']}.", "success")
        return redirect(url_for("events.admin_index"))
    return render_template(
        "events/admin/form.html", event=None, known_groups=_known_groups()
    )


@events_bp.route("/admin/events/<int:event_id>/edit", methods=["GET", "POST"])
@login_required
def admin_edit(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == "POST":
        data = _form_to_data(request.form)
        if not data["title"]:
            flash("Title is required.", "danger")
            return redirect(url_for("events.admin_edit", event_id=event_id))
        if data["title"] != event.title:
            data["slug"] = _unique_slug(data["title"], exclude_id=event.id)
        for key, value in data.items():
            setattr(event, key, value)
        db.session.commit()
        flash(f"Updated {event.title}.", "success")
        return redirect(url_for("events.admin_index"))
    return render_template(
        "events/admin/form.html", event=event, known_groups=_known_groups()
    )


@events_bp.route("/admin/events/<int:event_id>/move", methods=["POST"])
@login_required
def admin_move(event_id):
    event = Event.query.get_or_404(event_id)
    new_group = (request.form.get("group") or "").strip()
    if new_group and new_group != event.kind:
        event.kind = new_group
        db.session.commit()
        flash(f"Moved {event.title} to {new_group}.", "success")
    return redirect(url_for("events.admin_index"))


@events_bp.route("/admin/events/<int:event_id>/delete", methods=["POST"])
@login_required
def admin_delete(event_id):
    event = Event.query.get_or_404(event_id)
    title = event.title
    db.session.delete(event)
    db.session.commit()
    flash(f"Removed {title}.", "success")
    return redirect(url_for("events.admin_index"))
