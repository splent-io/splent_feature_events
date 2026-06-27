from flask_wtf import FlaskForm
from wtforms import SubmitField


class SplentFeatureEventsForm(FlaskForm):
    submit = SubmitField("Save splent_feature_events")
