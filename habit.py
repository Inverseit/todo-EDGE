import os
from flask import Flask, request
import telebot
types = telebot.types

NOT_STARTED = 0
DOING = 1
DONE  = 2

crossIcon = u"\u274C"
DoingIcon = "Doing"
Done = "Done"

TOKEN = '1125338216:AAFCOL_6RJYDPaSNNJEd3QAazK8yPUlNFDo'

server = Flask(__name__)

tasks = {}

bot = telebot.TeleBot(TOKEN)

def makeKeyboard():
    markup = types.InlineKeyboardMarkup()
    for key, value in tasks.items():
        markup.add(types.InlineKeyboardButton(text=value,
                                              callback_data="['value', '" + value + "', '" + key + "']"),
        types.InlineKeyboardButton(text=crossIcon,
                                   callback_data="['key', '" + key + "']"))
    return markup

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Hey let's get started!") # add some text


@bot.message_handler(commands=['add'])
def start_message(message):
    m = bot.send_message(message.chat.id, 'Hello, what task do you want to do today?')
    bot.register_next_step_handler(m, process_habit_step)
def process_habit_step(message):
    bot.send_message(message.chat.id, "Adding '{}' habit to your list".format(message.text))
    if message.text not in tasks.keys():
        tasks[message.text] = NOT_STARTED
        bot.send_message(message.chat.id, "Done! We added a new task: '{}'".format(message.text))
    else:
        bot.send_message(message.chat.id, "Sorry, you are already have task called '{}'".format(message.text))

@bot.message_handler(commands=['show'])
def start_message(message):
    if len(tasks.keys())==0:
        bot.send_message(message.chat.id, "😱 You didn't added any tasks, please click to the /add")
    else:
        bot.send_message(message.chat.id, "Here you are!",reply_markup=makeKeyboard())

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):

    if (call.data.startswith("['value'")):
        print(f"call.data : {call.data} , type : {type(call.data)}")
        print(f"ast.literal_eval(call.data) : {ast.literal_eval(call.data)} , type : {type(ast.literal_eval(call.data))}")
        valueFromCallBack = ast.literal_eval(call.data)[1]
        keyFromCallBack = ast.literal_eval(call.data)[2]
        bot.answer_callback_query(callback_query_id=call.id,
                              show_alert=True,
                              text="You Clicked " + valueFromCallBack + " and key is " + keyFromCallBack)

    if (call.data.startswith("['key'")):
        keyFromCallBack = ast.literal_eval(call.data)[1]
        del stringList[keyFromCallBack]
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Here are the values of stringList",
                              message_id=call.message.message_id,
                              reply_markup=makeKeyboard(),
                              parse_mode='HTML')



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