from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField
from wtforms.validators import Length

from database.data_engine import goals, spend_time

class BookingForm(FlaskForm):
    weekday = StringField()
    time = StringField()
    teacher = IntegerField()
    name = StringField("Вас зовут", [Length(min=3)])
    phone = IntegerField("Ваш телефон", [Length(min=4)])

class RequestForm(FlaskForm):
    goal_choices = [(key, value) for key, value in goals.items()]
    spend_time_choices = [(key, value) for key, value in spend_time.items()]
    spend_time = RadioField('Сколько времени есть?', choices=spend_time_choices)
    goal = RadioField('Какая цель занятий?', choices=goal_choices)
    name = StringField("Вас зовут", [Length(min=3)])
    phone = IntegerField("Ваш телефон", [Length(min=14)])