import telebot
import time
from telebot import types
import logging
from datetime import datetime
from pymongo import MongoClient
from config import TOKEN, MONGO
from data.models import Session, Users

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='sample.log', level=logging.ERROR, format=FORMAT)
bot = telebot.TeleBot(TOKEN)
client = MongoClient(MONGO)
db = client.test
users = db['users']
keyboard1 = types.ReplyKeyboardMarkup()
keyboard1.row('Начать день')
keyboard2 = types.ReplyKeyboardMarkup()
keyboard2.row('Ответить')
Time = time.ctime()
n = 0


@bot.message_handler(commands=['start'])
def start_message(message):
    now = datetime.now()
    msg = bot.send_message(message.chat.id, "Привет, отправь логин")
    point = 100
    bot.register_next_step_handler(msg, login, now, point)


def login(message, now, point):
    postgres = Session()
    print(now)
    print(point)
    try:
        obj = postgres.query(Users).filter(Users.login == str(message.text)).one()
        print(obj)
        postgres.close()
        msg = bot.send_message(message.chat.id, f'Please, enter your password {now.hour} {point}')
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
        now1 = datetime.now()
        sec = now1.second
        msg = bot.send_message(message.chat.id, 'Good morning', reply_markup=keyboard1)
        bot.register_next_step_handler(msg, vic, sec)
    except Exception as e:
        logging.error(Exception)
        print(e)
        msg = bot.send_message(message.chat.id, "Your password doesn't correct please send again")
        bot.register_next_step_handler(msg, pas)


def vic(message):
    # now = datetime.now()
    # sec = now.second
    msg = bot.send_message(message.chat.id, "Ответьте на вопрос в течении 20 секунд\nГлубина Марианской впдадины?",
                           reply_markup=keyboard2)
    qwe = bot.register_next_step_handler(msg, ans)
    print(qwe)


def ans(message, point=100):
    time.sleep(5)
    now = datetime.now()
    if 6 <= now.hour <= 7:
        time.sleep(180)
        point -= 1
    answer = message.text
    print(answer)
    print(point)


if __name__ == '__main__':
    bot.polling()
