import telebot
import database
from secret import token

bot = telebot.TeleBot(token)


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

bot.infinity_polling()
