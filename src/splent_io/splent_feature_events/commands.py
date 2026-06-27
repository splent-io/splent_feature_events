"""
CLI commands contributed by splent_feature_events.

These commands are auto-discovered by the framework and exposed in the
SPLENT CLI under the ``feature:events`` group.

Usage::

    splent feature:events hello
"""

import click


@click.command("hello")
def hello():
    """Example command — replace with your own."""
    click.echo("  Hello from splent_feature_events!")


cli_commands = [hello]
