import telebot
import database
from secret import token

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
    txt = 'Расписание экзаменов\n'
    for i in database.Exams.read_all():
        txt += f'{i[0]} - {i[1]}\n'
    bot.send_message(message.chat.id, txt)


@bot.message_handler(commands=["испытания"])
def entrance_tests(message):
    id = int(get_arguments(message)[0])
    if id is None:
        return

    speciality = database.Specialties.read(id)
    txt = f"Вступительные испытания для специальности {speciality[1]} - {', '.join(speciality[2:])}"
    bot.send_message(message.chat.id, txt)


@bot.message_handler(commands=["студент"])
def student(message):
    student_id = int(get_arguments(message)[0])
    txt = 'сумма баллов по каждой специальности:\n'
    print(student_id)

    for field in [i for i in database.Applications.read_all() if i[0] == student_id]:
        speciality = database.Specialties.read(field[1])[1]
        txt += f'{speciality} - {sum(field[2:])}\n'

    bot.send_message(message.chat.id, txt)


print('бот запущен')
bot.infinity_polling()
