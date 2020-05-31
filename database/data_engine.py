from database.data import goals, teachers
from database.models import db, Teacher, Goal, Schedule

db.create_all()

for key, value in goals.items():
    goal = Goal(id=key, translate_name=value[0], emoji=value[1])
    db.session.add(goal)

for item in teachers:
    teacher = Teacher(
        id=item['id'],
        name=item['name'],
        about=item['about'],
        rating=item['rating'],
        picture=item['picture'],
        price=item['price'])

    for goal in item['goals']:
        raw_goal = Goal.query.get(goal)
        teacher.goals.append(raw_goal)

    for key, value  in item['free'].items():

        for key_time, value_time in value.items():
            if value_time == True:
                day = Schedule(
                    weekday=key,
                    id_teacher=item['id'],
                    time=key_time)
                db.session.add(day)

db.session.commit()
