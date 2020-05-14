import random


from flask import Flask, render_template, request, redirect

from database.data_engine import Teacher, goals, DataBase, TeachersFilter, days_translate, spend_time
from forms import BookingForm, RequestForm

app = Flask(__name__)
app.secret_key = 'super'


@app.route('/')
def render_main():
    teacher_quantity = len(DataBase().teacher_quantity)
    random_teacher_list = [Teacher(i).teacher_data_generator() for i in random.sample(range(teacher_quantity - 1), 3)]
    return render_template('index.html', random_teacher_list=random_teacher_list, goals=goals)


@app.route('/goals/<goal>/')
def render_goal(goal):
    goal_to_read = goals[goal]
    teacher_list = TeachersFilter().specific_teachers(goal)
    return render_template('goal.html', goal_to_read=goal_to_read, random_teacher_list=teacher_list)


@app.route('/booking/<int:id_teacher>/<week_day>/<time>/', methods=["GET", "POST"])
def render_booking(id_teacher, week_day, time):
    teacher = Teacher(id_teacher)
    teacher_data = teacher.teacher_data_generator()
    form = BookingForm()
    form.weekday.data = week_day
    form.time.data = time
    form.teacher.data = id_teacher
    if form.validate_on_submit():
        teacher.teacher_change_schedule(id_teacher, week_day, time, form.name.data, form.phone.data)
        user_data = f'?id={id_teacher}&wd={week_day}&t={time}&n={form.name.data}&p={form.phone.data}'

        return redirect('/booking_done/' + user_data, code=302)
    else:
        return render_template('booking.html', teacher_data=teacher_data, week_day=week_day, time=time, form=form)


@app.route('/booking_done/', methods=["GET"])
def render_booking_done():
    name = request.args['n']
    phone = request.args['p']
    weekday = request.args['wd']
    weekday_translate = days_translate[weekday]
    time = request.args['t']
    teacher = request.args['id']
    raw_teacher = Teacher(int(teacher))
    teacher_name = raw_teacher.teacher_data_generator()['name']

    return render_template('booking_done.html', name=name, phone=phone, weekday=weekday_translate, time=time,
                           teacher=teacher_name)


@app.route('/profiles/<int:id_teacher>/')
def render_profile(id_teacher):
    teacher = Teacher(id_teacher)
    teacher_data = teacher.teacher_data_generator()
    teacher_schedule = teacher.teacher_schedule_generator()
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


@app.route('/tutor_list/')
def render_tutor_list():
    teacher_list = TeachersFilter().all_teachers()
    return render_template('tutor_list.html', random_teacher_list=teacher_list)


if __name__ == '__main__':
    app.run()
