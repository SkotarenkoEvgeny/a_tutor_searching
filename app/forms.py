from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField
from wtforms.validators import Length

from database.data_engine import goals

class BookingForm(FlaskForm):
    weekday = StringField()
    time = StringField()
    teacher = IntegerField()
    name = StringField("Вас зовут", [Length(min=3)])
    phone = IntegerField("Ваш телефон", [Length(min=14)])

class RequestForm(FlaskForm):
    goal_choices = [(key, value) for key, value in goals.items()]
    spend_time = RadioField('Сколько времени есть?', choices=[(2, '1-2 часа'), (5, '3-5 часов'), (7, '5-7 часов'), (10, '7-10 часов')])
    goal = RadioField('Какая цель занятий?', choices=goal_choices)
    name = StringField("Вас зовут", [Length(min=3)])
    phone = IntegerField("Ваш телефон", [Length(min=14)])