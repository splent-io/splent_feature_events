from flask import request, url_for

from splent_framework.hooks.template_hooks import register_template_hook


def events_admin_link():
    """Sidebar entry for the Events management screen (the WP-plugin pattern)."""
    active = (
        "active"
        if request.endpoint and request.endpoint.startswith("events.admin")
        else ""
    )
    return (
        f'<li class="sidebar-item {active}">'
        f'<a class="sidebar-link" href="{url_for("events.admin_index")}">'
        '<i class="align-middle" data-feather="calendar"></i> '
        '<span class="align-middle">Events</span>'
        "</a>"
        "</li>"
    )


register_template_hook("layout.authenticated_sidebar", events_admin_link)
