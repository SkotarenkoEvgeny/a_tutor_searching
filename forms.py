from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, IntegerField
from wtforms.validators import Length, Regexp


goals = {"travel": ["Для путешествий", '⛱'], "study": ["Для учебы", '📖'], "work": ["Для работы", '🛠️'],
         "relocate": ["Для переезда", '🚜'], 'prog': ['Для програмирования', '💻']}
spend_time = {2: '1-2 часа', 5: '3-5 часов', 7: '5-7 часов', 10: '7-10 часов'}

class BookingForm(FlaskForm):
    weekday = StringField()
    time = StringField()
    teacher = IntegerField()
    name = StringField("Вас зовут", [Length(min=3)])
    phone = StringField("Ваш телефон", [
        Regexp(r'\+[\d]{2}-[\d]{3}-[\d]{3}-[\d]{2}-[\d]{2}', message='Введите согласно шаблона +00-000-000-00-00')])


class RequestForm(FlaskForm):
    goal_choices = [(key, value[0]) for key, value in goals.items()]
    spend_time_choices = [(key, value) for key, value in spend_time.items()]
    spend_time = RadioField('Сколько времени есть?', choices=spend_time_choices)
    goal = RadioField('Какая цель занятий?', choices=goal_choices)
    name = StringField("Вас зовут", [Length(min=3)])
    phone = StringField("Ваш телефон", [
        Regexp(r'\+[\d]{2}-[\d]{3}-[\d]{3}-[\d]{2}-[\d]{2}', message='Введите согласно шаблона +00-000-000-00-00')])
