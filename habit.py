import os
import ast
import time
from flask import Flask, request
import telebot
types = telebot.types

# used constants
NOT_STARTED = 0
DOING = 1
DONE  = 2

crossIcon =  "❌"
not_started_icon = "🆕"
doing_icon = "🕗"
done_icon = "✅"

# TOKEN = '1125338216:AAFCOL_6RJYDPaSNNJEd3QAazK8yPUlNFDo'
TOKEN = '1332982455:AAHvLsgv5NG9anh2OdY2o7-66c36rea5wXA'

server = Flask(__name__)

tasks = {}

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Hey let's get started! Type / to see all availabe commands") # add some text

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, "In show menu \n {0} is new tasks \n {1} is tasks in progress \n {2} is finished task \n Press {3} to delete the task".format(not_started_icon, doing_icon, done_icon,crossIcon )) # add some text


@bot.message_handler(commands=['add'])
def start_message(message):
    m = bot.send_message(message.chat.id, 'What task do you want to add to your today list?')
    bot.register_next_step_handler(m, process_habit_step)
def process_habit_step(message):
    bot.send_message(message.chat.id, "Adding '{}' habit to your list.....".format(message.text))
    if message.text not in tasks.keys():
        tasks[message.text] = NOT_STARTED
        bot.send_message(message.chat.id, "Done! We added a new task: '{}'".format(message.text))        
    else:
        m = bot.send_message(message.chat.id, "Sorry, you are already have task called '{}'".format(message.text))
        bot.register_next_step_handler(m, start_message)


def makeKeyboard():
    markup = types.InlineKeyboardMarkup()
    for key, value in tasks.items():
        icon = not_started_icon
        if value == DOING:
            icon = doing_icon
        elif value == DONE:
            icon = done_icon
        markup.add(
            types.InlineKeyboardButton(text=icon+key, callback_data="['key', '{}']".format(key)),
            types.InlineKeyboardButton(text=crossIcon,callback_data="['del', '{}']".format(key))
        )
    return markup

@bot.message_handler(commands=['show'])
def start_message(message):
    if len(tasks.keys())==0:
        bot.send_message(message.chat.id, "😱 You didn't added any tasks, please click to the /add")
    else:
        bot.send_message(message.chat.id, "Here you are!",reply_markup=makeKeyboard())


@bot.message_handler(commands=['done'])
def start_message(message):
    text = "Here is your list of {} \n".format(done_icon)
    added = False
    for key, value in tasks.items():
        if value != DONE:
            continue
        text +="**{0}**\n".format(key)
        added = True
    if not added:
        bot.send_message(message.chat.id, "You don't have any finished task. Let's do them")
    else:
        bot.send_message(message.chat.id, text)
        
@bot.message_handler(commands=['new'])
def start_message(message):
    text = "Here is your list of {} \n".format(not_started_icon)
    added = False
    for key, value in tasks.items():
        if value != NOT_STARTED:
            continue
        text +="**{0}**\n".format(key)
        added = True
    if not added:
        bot.send_message(message.chat.id, "You dont have any new tasks. Let's add them")
    else:
        bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['progress'])
def start_message(message):
    text = "Here is your list of {} \n".format(doing_icon)
    added = False
    for key, value in tasks.items():
        if value != DOING:
            continue
        text +="**{0}**\n".format(key)
        added = True
    if not added:
        bot.send_message(message.chat.id, "You don't have any current tasks. Let's start them")
    else:
        bot.send_message(message.chat.id, text)



@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if (call.data.startswith("['key'")):
        keyFromCallBack = ast.literal_eval(call.data)[1]
        tasks[keyFromCallBack] +=1
        if tasks[keyFromCallBack] > DONE:
            tasks[keyFromCallBack] = DONE
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Your tasks",
                              message_id=call.message.message_id,
                              reply_markup=makeKeyboard(),
                              parse_mode="HTML")

    if (call.data.startswith("['del'")):
        keyFromCallBack = ast.literal_eval(call.data)[1]
        del tasks[keyFromCallBack]
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Your tasks",
                              message_id=call.message.message_id,
                              reply_markup=makeKeyboard(),
                              parse_mode="HTML")


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