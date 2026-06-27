"""Alembic migration environment for splent_feature_events."""

from splent_io.splent_feature_events import models  # noqa
from splent_framework.migrations.feature_env import run_feature_migrations

FEATURE_NAME = "splent_feature_events"
FEATURE_TABLES = set()

run_feature_migrations(FEATURE_NAME, FEATURE_TABLES)
