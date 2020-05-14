import json, os

goals = {"travel": ["Для путешествий", '⛱'], "study": ["Для учебы", '📖'], "work": ["Для работы", '🛠️'],
         "relocate": ["Для переезда", '🚜'], 'prog': ['Для програмирования', '💻']}
days_translate = {'mon': 'Понедельник', 'tue': 'Второник', 'wed': 'Среда', 'thu': 'Четверг', 'fri': 'Пятница',
                  'sat': 'Субота', 'sun': 'Воскресенье'}
spend_time = {2: '1-2 часа', 5: '3-5 часов', 7: '5-7 часов', 10: '7-10 часов'}
base_dir = '../app/database'


class DataBase:

    def __init__(self):
        self.database = DataBase.read_db()
        self.teacher_quantity = [i.get('id') for i in self.database]

    def check_file(self, file_name):
        return os.path.exists(os.path.join(base_dir, file_name))

    @classmethod
    def read_db(cls):
        with open('../app/database/database.json', 'r') as f:
            teachers = json.load(f)
        return teachers

    def write_db(self, data):
        with open('../app/database/database.json', 'w') as f:
            json.dump(data, f)

    @staticmethod
    def json_worker(file_name, new_data):
        if os.path.exists(os.path.join(base_dir, file_name)):
            with open(os.path.join(base_dir, file_name), 'r') as f:
                data = json.load(f)
            data.append(new_data)
            with open(os.path.join(base_dir, file_name), 'w') as f:
                json.dump(data, f)
        else:
            data = []
            data.append(new_data)
            with open(os.path.join(base_dir, file_name), 'w') as f:
                json.dump(data, f)


class Teacher(DataBase):

    def __init__(self, id_teacher):
        super().__init__()
        self.raw_teacher_data = [i for i in self.database if i.get('id') == id_teacher][0]

    def teacher_data_generator(self):
        data_list = ['id', 'name', 'about', 'picture', 'rating', 'price']
        teacher_data = {key: value for (key, value) in self.raw_teacher_data.items() if key in data_list}
        teacher_data['goals'] = [goals[key] for key in goals.keys() if key in self.raw_teacher_data['goals']]
        return teacher_data

    def teacher_schedule_generator(self):
        schedule = {}
        raw_schedule = self.raw_teacher_data["free"]
        for key, value in raw_schedule.items():
            day = days_translate[key]
            schedule[day] = (list(filter(lambda i: value[i] is not False, value)), key)
        return schedule

    def teacher_change_schedule(self, teacher, weekday, time, name, phone):
        print(teacher, weekday, time, name, phone)
        for item in self.database:
            if item['id'] == teacher:
                item['free'][weekday][time] = False
                self.write_db(self.database)
                data = {"teacher": teacher, "weekday": weekday, "time": time, "name": name, "phone": phone}
                self.json_worker('booking.json', data)


class TeachersFilter(DataBase):

    def __init__(self):
        super().__init__()

    def specific_teachers(self, goal):
        data = [Teacher(i.get('id')).teacher_data_generator() for i in self.database
                if goal in i.get('goals')]
        data.sort(key=lambda i: i['rating'], reverse=True)
        return data

    def goals_list(self):
        goals_list = {}
        for key, value in goals.items():
            goals_list[value] = TeachersFilter.specific_teachers(self, key)
        return goals_list

    def all_teachers(self):
        return [Teacher(i).teacher_data_generator() for i in self.teacher_quantity]
