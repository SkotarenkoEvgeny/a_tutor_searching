from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

teachers_goals_association = db.Table('teachers_goals',
                                      db.Column('teachers_id', db.Integer, db.ForeignKey('teachers.id')),
                                      db.Column('goal_id', db.String, db.ForeignKey('goals.id')))


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Name', db.String, nullable=False)
    about = db.Column('About', db.String, nullable=False)
    rating = db.Column('Rating', db.Float, nullable=False)
    picture = db.Column('Picture', db.String, nullable=False)
    price = db.Column('Price', db.Integer)
    goals = db.relationship('Goal', secondary=teachers_goals_association, back_populates="teachers")
    teacher_schedule = db.relationship('Schedule')


class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.String, primary_key=True, unique=True)
    translate_name = db.Column(db.String, nullable=False)
    emoji = db.Column(db.String, nullable=False)
    teachers = db.relationship("Teacher", secondary=teachers_goals_association, back_populates="goals")


class Schedule(db.Model):
    __tablename__ = 'Schedule'

    id = db.Column(db.Integer, primary_key=True)
    id_teacher = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    weekday = db.Column(db.String)
    time = db.Column(db.Time)


    # def __repr__(self):
    #     print(self.list)
    #     return self.list


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    id_teacher = db.Column(db.Integer)
    weekday = db.Column(db.String)
    time = db.Column(db.String)
    name = db.Column(db.String)
    phone = db.Column(db.String)


days_translate = {'mon': 'Понедельник', 'tue': 'Второник', 'wed': 'Среда', 'thu': 'Четверг', 'fri': 'Пятница',
                  'sat': 'Субота', 'sun': 'Воскресенье'}

time_template = {'8:00': 8, '10:00': 10, '12:00': 12, '14:00': 14, '16:00': 16, '18:00': 18, '20:00': 20}


def data_preparing(query_list):
    """
    :param query_list: [<Teacher 5>]
    :return: {'Понедельник': ['16:00', '20:00', '18:00'], 'Второник': ['16:00', '20:00', '18:00']}
    """

    schedule = {}
    for item in query_list:
        raw_dict = item.__dict__
        day = days_translate[raw_dict['weekday']]
        temp_list = []
        for i in raw_dict.keys():
            temp_data = time_template.get(i, None)
            if temp_data is not None:
                if raw_dict[i] != False:
                    temp_list.append(time_template[i])
        schedule[day] = temp_list
    return schedule


def day_reverse(day):
    """
    :param day: day about russian
    :return: day for DB
    """

    for key, value in days_translate.items():
        if day == value:
            return key

def time_reverse(time):
    """
    :param day: day about russian
    :return: day for DB
    """

    for key, value in time_template.items():
        if time == value:
            return key