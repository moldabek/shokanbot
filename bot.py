import telebot
import time
from telebot import types
import logging
from datetime import datetime
from pymongo import MongoClient
from config import TOKEN, MONGO
from data.models import Session, Users
import schedule


FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='sample.log', level=logging.ERROR, format=FORMAT)
bot = telebot.TeleBot(TOKEN)
client = MongoClient(MONGO)
db = client.test
users = db['users']
keyboard1 = types.ReplyKeyboardMarkup()
keyboard2 = types.KeyboardButton('Доброе утро')
keyboard1.add(keyboard2)
Time = time.ctime()
n = 0


@bot.message_handler(commands=['start'])
def start_message(message):
    # now = datetime.now()
    msg = bot.send_message(message.chat.id, "Привет, отправь логин")
    # point = 100
    bot.register_next_step_handler(msg, login)


def login(message):
    postgres = Session()
    try:
        obj = postgres.query(Users).filter(Users.login == str(message.text)).one()
        print(obj)
        postgres.close()
        msg = bot.send_message(message.chat.id, f'Please, enter your password')
        bot.register_next_step_handler(msg, pas)
        # data = message.text.split()
        # print(data)
        # print(data[0])
        # print(data[1])
        # check = users.find_one({
        #     'username': data[0],
        #     'password': data[1],
        # })
        #
        # if check is None:
        #     msg = bot.send_message(message.chat.id, r'Неправильно введен логин\пароль')
        #     bot.send_message(message.chat.id, "Please, send me again your login & pass")
        #     bot.register_next_step_handler(msg, login)
        # else:
        #     msg = bot.send_message(message.chat.id, 'Good morning', reply_markup=keyboard1)
        #     bot.register_next_step_handler(msg, vic)
    except Exception as e:
        logging.error("Exception")
        print(e)
        msg = bot.send_message(message.chat.id, "You're login invalid or you aren't a participated this course")
        bot.register_next_step_handler(msg, login)


def pas(message):
    post = Session()
    try:
        obj = post.query(Users).filter(Users.password == str(message.text)).one()
        print(obj)
        post.close()
        msg = bot.send_message(message.chat.id, 'Good morning', reply_markup=keyboard1)
        bot.register_next_step_handler(msg, vic)
    except Exception as e:
        logging.error(Exception)
        print(e)
        msg = bot.send_message(message.chat.id, "Your password doesn't correct please send again")
        bot.register_next_step_handler(msg, pas)


def vic(message):
    now = datetime.now()
    msg = bot.send_message(message.chat.id, "Ответьте на вопрос после 20-ти секунд\nГлубина Марианской впдадины?")
    send = bot.send_message(message.chat.id, 'Осталось : 20')
    for i in range(19, -1, -1):
        time.sleep(1)
        bot.edit_message_text(f'Осталось : {i}', message.chat.id, send.message_id)
    bot.send_message(message.chat.id, "Жду ответа :)")
    bot.register_next_step_handler(msg, ans)


def ans(message):
    bot.send_message(message.chat.id, "Ответ принят")
    answer = message.text
    print(answer)


@bot.message_handler(content_types=['photo', 'file'])
def screenshotcheker(message):
    bot.send_message(message.chat.id, "Thank you for using our bot")


if __name__ == '__main__':
    bot.polling()
