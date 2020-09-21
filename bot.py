import threading
import telebot
import time
from telebot import types
import logging
from datetime import datetime
from config import TOKEN
from data.models import Session
from sqlalchemy import table, column

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='sample.log', level=logging.ERROR, format=FORMAT)
bot = telebot.TeleBot(TOKEN)
users = {'bilbao': '26'}

keyboard1 = types.ReplyKeyboardMarkup()
keyboard2 = types.KeyboardButton('Доброе утро')
keyboard1.add(keyboard2)
Time = time.ctime()
n = 0


@bot.message_handler(commands=['start'])
def start_message(message):
    # now = datetime.now()
    msg = bot.send_message(message.chat.id, "Введите логин: ")
    # point = 100
    bot.register_next_step_handler(msg, login)


def login(message):
    try:
        # obj = postgres.query(Users).filter(Users.login == str(message.text)).one()
        # print(obj)
        # postgres.close()
        data = message.text.split()
        print(data)
        print(data[0])
        print(data[1])

        if users[data[0]] != data[1]:
            msg = bot.send_message(message.chat.id, r'Неправильно введен логин\пароль')
            bot.register_next_step_handler(msg, login)
        else:
            msg = bot.send_message(message.chat.id, 'Good morning', reply_markup=keyboard1)
            bot.register_next_step_handler(msg, vic)

    except Exception as e:
        logging.error("Exception")
        print(e)
        msg = bot.send_message(message.chat.id, "You're login invalid or you aren't a participated this course")
        bot.register_next_step_handler(msg, login)


def timer(chat_id, message_id):
    for i in range(19, -1, -1):
        time.sleep(1)
        bot.edit_message_text(f'Осталось : {i}', chat_id, message_id)


def ans(message):
    print(message)
    print("check")
    if message.text == "15":
        bot.send_message(message.chat.id, "Верно!")
        msg = bot.send_message(message.chat.id, "Отправьте скрин инста-сториза :)")
        bot.register_next_step_handler(msg, screenshotcheker)


def vic(message):
    bot.send_message(message.chat.id, "Ответьте на вопрос в течении 20-ти секунд\nГлубина Марианской впдадины?")
    send = bot.send_message(message.chat.id, 'Осталось : 20')
    x = threading.Thread(target=timer, args=(message.chat.id, send.message_id))
    x.start()
    bot.register_next_step_handler(send, ans)


@bot.message_handler(content_types=['photo', 'file'])
def screenshotcheker(message):
    postgres = Session()
    score = 100
    now = datetime.now()
    username = message.from_user.username
    chat_id = message.chat.id
    t = table('scores', column("id"), column("username"), column("score"))
    t.insert().values(id=chat_id, username=f'{username}', score=score)
    bot.send_message(message.chat.id, "Thank you for using our bot")


if __name__ == '__main__':
    bot.polling()
