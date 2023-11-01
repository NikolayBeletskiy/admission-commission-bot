import telebot
import database
from secret import token


def get_exams_txt():
    txt = ''
    for i in database.Exams.read_all():
        txt += f'{i[0]} - {i[1]}\n'
    return txt


def get_tests_txt(id):
    speciality = database.Specialties.read(id)
    return f"{speciality[1]} - {', '.join(speciality[2:])}"


def get_points_of_specialities_txt(id):
    txt = ''
    for field in [i for i in database.Applications.read_all() if i[0] == id]:
        speciality = database.Specialties.read(field[1])
        txt += f'{speciality[1]} - {sum(field[2:])}\n'
    return txt


def get_points_of_subjects_txt(id):
    txt = ''
    subjects = {}
    for field in [i for i in database.Applications.read_all() if i[0] == id]:
        speciality = database.Specialties.read(field[1])
        for i, v in zip(speciality[2:], field[2:]):
            subjects[i] = v
    for i in subjects:
        txt += f"{i} - {subjects[i]}\n"
    return txt


bot = telebot.TeleBot(token)


def get_arguments(message) -> tuple[str, ...]:
    args = message.text.split()[1:]
    if len(args) == 0:
        bot.send_message(message.chat.id, "требуются аргументы команды")
        return
    return tuple(args)


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "привет")


@bot.message_handler(commands=["help"])
def help_message(message):
    bot.send_message(message.chat.id, '''
    доступные команды:
    /студент [номер заявления]
    /расписание
    /испытания [номер специальности]
    ''')


@bot.message_handler(commands=["расписание"])
def exam_schedule(message):
    txt = f'Расписание экзаменов\n{get_exams_txt()}'
    bot.send_message(message.chat.id, txt)


@bot.message_handler(commands=["испытания"])
def entrance_tests(message):
    id = int(get_arguments(message)[0])
    if id is None:
        return

    txt = f"Вступительные испытания для специальности {get_tests_txt(id)}"
    bot.send_message(message.chat.id, txt)


@bot.message_handler(commands=["студент"])
def student(message):
    student_id = int(get_arguments(message)[0])
    if student_id is None:
        return
    txt1 = f"оценки по предметам: \n{get_points_of_subjects_txt(student_id)}"
    txt2 = f'сумма баллов по каждой специальности:\n{get_points_of_specialities_txt(student_id)}'

    bot.send_message(message.chat.id, txt1)
    bot.send_message(message.chat.id, txt2)


print('бот запущен')
bot.infinity_polling()
