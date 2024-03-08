from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms import EmailField, SubmitField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    title = StringField("Depart title", validators=[DataRequired()])
    chief = IntegerField("Chief id", validators=[DataRequired()])
    members = TextAreaField("Members ID-s", validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired()])
    submit = SubmitField('Submit')
