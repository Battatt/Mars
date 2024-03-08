from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms import DateTimeField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    team_leader = IntegerField("Team Leader Id", validators=[DataRequired()])
    job = StringField("Job description", validators=[DataRequired()])
    work_size = IntegerField("Work size in hour", validators=[DataRequired()])
    collaborators = TextAreaField("Collaborators ID-s", validators=[DataRequired()])
    start_date = DateTimeField("Start date")
    end_date = DateTimeField("End date")
    is_finished = BooleanField("Is finished?")
    submit = SubmitField('Submit')
