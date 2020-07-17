import os
from flask import Flask, request
import telebot

TOKEN = '1125338216:AAFCOL_6RJYDPaSNNJEd3QAazK8yPUlNFDo'
# bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
print("here")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')

@bot.message_handler(content_types=['text'])
def send_text(message):
    print(message.text.lower() + " is revieved")
    if message.text.lower() == 'привет':
        msg = bot.send_message(message.chat.id, 'Привет, мой создатель')
        bot.register_next_step_handler(msg, process_name_step)
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    def process_name_step(message):
        bot.send_message(message.chat.id, 'Проверяю следующие возможности')

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