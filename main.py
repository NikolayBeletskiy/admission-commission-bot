import telebot
from telebot import types
import database
from secret import token


def create_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("расписание")
    item2 = types.KeyboardButton("студент")
    item3 = types.KeyboardButton("испытания")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    return markup


def get_exams_txt():
    txt = ''
    for i in database.Exams.read_all():
        txt += f'{i[0]} - {i[1]}\n'
    return txt


def get_tests_txt(id):
    subjects = set()
    for field in [i for i in database.Applications.read_all() if i[0] == id]:
        speciality = database.Specialties.read(field[1])
        subjects.update(set(speciality[2:]))
    txt = ', '.join(subjects)
    return txt


def get_points_of_specialities_txt(id):
    txt = ''
    specialties = {}
    for field in [i for i in database.Applications.read_all() if i[0] == id]:
        speciality = database.Specialties.read(field[1])
        specialties[speciality[1]] = sum(field[2:])
    for i in specialties:
        txt += f"{i} - {specialties[i]}\n"
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


def get_student_id(chat_id):
    return database.Chats.read(chat_id)[1]


@bot.message_handler(commands=["start"])
def start_message(message):
    if database.Chats.read(message.chat.id) is None:
        database.Chats.create(message.chat.id)
        bot.send_message(message.chat.id, "Чтобы выбрать номер заявки используйте команду /setstudentid")
    else:
        bot.send_message(message.chat.id, 'Здраствуйте', reply_markup=create_buttons())


@bot.message_handler(commands=["setstudentid"])
def set_student_id(message):
    student_id = int(get_arguments(message)[0])
    database.Chats.set_student_id(message.chat.id, student_id)

    bot.send_message(message.chat.id, 'Номер заявки сохранён', reply_markup=create_buttons())


@bot.message_handler(commands=["расписание"])
def exam_schedule(message):
    txt = f'Расписание экзаменов\n{get_exams_txt()}'
    bot.send_message(message.chat.id, txt)


@bot.message_handler(commands=["испытания"])
def entrance_tests(message):
    student_id = get_student_id(message.chat.id)
    txt = f"Вступительные испытания:\n{get_tests_txt(student_id)}"
    bot.send_message(message.chat.id, txt)


@bot.message_handler(commands=["студент"])
def student(message):
    student_id = get_student_id(message.chat.id)

    txt1 = f"оценки по предметам: \n{get_points_of_subjects_txt(student_id)}"
    txt2 = f'сумма баллов по каждой специальности:\n{get_points_of_specialities_txt(student_id)}'

    bot.send_message(message.chat.id, txt1)
    bot.send_message(message.chat.id, txt2)


print('бот запущен')
bot.infinity_polling()
