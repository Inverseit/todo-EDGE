import os
from flask import Flask, request
import telebot

TOKEN = '1125338216:AAFCOL_6RJYDPaSNNJEd3QAazK8yPUlNFDo'
# bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
print("here")

bot = telebot.TeleBot('1125338216:AAFCOL_6RJYDPaSNNJEd3QAazK8yPUlNFDo')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')

@bot.message_handler(content_types=['text'])
def send_text(message):
    print(message.text.lower() + " is revieved")
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')

@bot.message_handler(content_types=['photo'])
def send_text(message):
    bot.send_message(message.chat.id, 'красиво!')



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