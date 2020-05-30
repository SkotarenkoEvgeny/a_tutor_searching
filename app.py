import random


from flask import Flask, render_template, request, redirect

from database.models import db, Teacher, Goal, Schedule, Booking, data_preparing, day_reverse
from forms import BookingForm, RequestForm

app = Flask(__name__)
app.secret_key = 'super'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutor-db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)




# models

# with app.app_context():
#     db.create_all()
#
#     for key, value in goals.items():
#         goal = Goal(id=key, translate_name=value[0], emoji=value[1])
#         db.session.add(goal)
#
#     for item in teachers:
#         teacher = Teacher(
#             id=item['id'],
#             name=item['name'],
#             about=item['about'],
#             rating=item['rating'],
#             picture=item['picture'],
#             price=item['price'])
#
#         for goal in item['goals']:
#             raw_goal = Goal.query.get(goal)
#             teacher.goals.append(raw_goal)
#
#         for key, value  in item['free'].items():
#
#             for key_time, value_time in value.items():
#                 if value_time == True:
#                     day = Schedule(
#                         weekday=key,
#                         id_teacher=item['id'],
#                         time=key_time
#                     )
#                     db.session.add(day)
#
#     db.session.commit()

# complete
@app.route('/')
def render_main():
    random_teacher_list = random.choices(db.session.query(Teacher).all(), k=3)
    return render_template('index.html', random_teacher_list=random_teacher_list, goals=Goal.query.all())


@app.route('/goals/<goal>/')
def render_goal(goal):
    goal_to_read = Goal.query.get(goal)
    teacher_list = Teacher.query.filter(Goal.id == goal)
    return render_template('goal.html', goal=goal_to_read.translate_name, goal_emoji=goal_to_read.emoji, random_teacher_list=teacher_list)

# complete
@app.route('/booking/<int:id_teacher>/<week_day>/<time>/', methods=["GET", "POST"])
def render_booking(id_teacher, week_day, time):
    print(id_teacher, week_day, time)
    teacher = Teacher.query.get(id_teacher)
    form = BookingForm()
    form.weekday.data = week_day
    form.time.data = time
    form.teacher.data = id_teacher
    edited_schedule = Schedule.query.filter(db.and_(Schedule.id_teacher == id_teacher, Schedule.weekday == day_reverse(week_day), Schedule.time == time)).first()

    if form.validate_on_submit():
        reverse_day = day_reverse(week_day)
        # current_db_sessions = db.session.object_session(edited_schedule)
        # db.session.delete(edited_schedule)
        db.session.commit()
        user_data = f'?id={id_teacher}&wd={reverse_day}&t={time}&n={form.name.data}&p={form.phone.data}'
        return redirect('/booking_done/' + user_data, code=302)
    else:
        return render_template('booking.html', teacher_data=teacher, week_day=week_day, time=time, form=form)

# complete
@app.route('/booking_done/', methods=["GET"])
def render_booking_done():
    name = request.args['n']
    phone = request.args['p']
    weekday = request.args['wd']
    time = request.args['t']
    teacher_id = request.args['id']
    raw_teacher = Teacher.query.get(teacher_id)
    booking = Booking(id_teacher = teacher_id,   weekday = weekday, time = time, name = name, phone = phone)
    db.session.add(booking)
    db.session.commit()
    return render_template('booking_done.html', name=name, phone=phone, weekday=day_reverse(weekday), time=time,
                           teacher=raw_teacher.name)

# complete
@app.route('/profiles/<int:id_teacher>/')
def render_profile(id_teacher):
    teacher_data = db.session.query(Teacher).get(id_teacher)
    teacher_schedule = data_preparing(Schedule.query.filter_by(id_teacher=id_teacher).all())
    return render_template('profile.html', teacher=teacher_data, teacher_schedule=teacher_schedule)



@app.route('/request/')
def render_request():
    form = RequestForm()
    return render_template('request.html', form=form)


@app.route('/request_done/', methods=["POST"])
def render_request_done():
    form = RequestForm()
    data = {"spend_time": form.spend_time.data, "goal": form.goal.data, "name": form.name.data,
            "phone": form.phone.data}
    DataBase.json_worker('request.json', data)
    data['goal'] = goals[form.goal.data]
    print(spend_time)
    print(form.spend_time.data)
    data['spend_time'] = spend_time[int(form.spend_time.data)]
    return render_template('request_done.html', data=data)

# complete
@app.route('/tutor_list/')
def render_tutor_list():
    teacher_list = Teacher.query.all()
    return render_template('tutor_list.html', random_teacher_list=teacher_list)


if __name__ == '__main__':
    app.run()
