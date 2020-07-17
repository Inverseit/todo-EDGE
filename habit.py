import os
from flask import Flask, request
import telebot
import myutils

TOKEN = '1125338216:AAFCOL_6RJYDPaSNNJEd3QAazK8yPUlNFDo'
# bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

class Task:
  def __init__(self, name, cid, number_of_time, motivation):
    self.name = name
    self.cid = cid
    self.number_of_time = number_of_time
    self.motivation = motivation
  def print_task(self):
    print("Name {0}, cid {1}, n is {2} and motiv: {3}".format(self.name, self.cid, self.number_of_time, self.motivation))

tasks = []

def generate_markup(list):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for item in list:
        markup.add(item)
    return markup

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')


@bot.message_handler(commands=['add'])
def start_message(message):
    m = bot.send_message(message.chat.id, 'Hello, what habit you want to track with me?')
    bot.register_next_step_handler(m, process_habit_step)
def process_habit_step(message):
    bot.send_message(message.chat.id, "Adding '{}' habit to your list".format(message.text))
    print(message)
    new_task = Task(message.text, message.chat.id,0,"Just do it")
    tasks.append(new_task)
    new_task.print_task()
    m = bot.send_message(message.chat.id, "Done! Current motivation message is '{}'. Do you want edit it?".format(new_task.motivation), reply_markup=generate_markup(["Yes", "No"]))
    bot.register_next_step_handler(m, process_motiv_step)
def process_motiv_step(message):
    if message.text == "Yes":
        m = bot.send_message(message.chat.id, 'Please enter new motivation text')
        bot.register_next_step_handler(m, process_change_motiv_step)
def process_change_motiv_step(message):
    tasks[-1].motivation = message.text
    m = bot.send_message(message.chat.id, "Done! Current motivation message is changed to **'{}'**".format(tasks[-1].motivation))


@bot.message_handler(commands=['show'])
def start_message(message):
    if len(tasks)!=0:
        m = bot.send_message(message.chat.id, "Please, choose habit:")
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        for task in tasks:
            bot.send_message(message.chat.id, "Here is '{}'".format(task.name))
            # print(task.name)
            markup.append(task.name)
        bot.register_next_step_handler(m, process_show_step, reply_markup=generate_markup(task_names_list))
    else:
        bot.send_message(message.chat.id, "😱Please add habits by entering \start")
def process_show_step(message):
    print("nts")

@bot.message_handler(content_types=['text'])
def send_text(message):
    print(message.text.lower() + " is revieved")
    if message.text.lower() == 'привет':
        msg = bot.send_message(message.chat.id, '')
        bot.register_next_step_handler(msg, process_name_step)
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
def process_name_step(message):
    bot.send_message(message.chat.id, "До")

@bot.message_handler(content_types=['photo'])
def send_text(message):
    bot.send_message(message.chat.id, 'красиво!')


# @bot.message_handler(commands=['help', 'start'])
# def send_welcome(message):
#     msg = bot.reply_to(message, """\
# Hi there, I am Example bot.
# What's your name?
# """)
#     bot.register_next_step_handler(msg, process_name_step)
  
  
# def process_name_step(message):
#     try:
#         chat_id = message.chat.id
#         name = message.text
#         user = User(name)
#         user_dict[chat_id] = user
#         msg = bot.reply_to(message, 'How old are you?')
#         bot.register_next_step_handler(msg, process_age_step)
#     except Exception as e:
# bot.reply_to(message, 'oooops')













@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://habitualforus.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))