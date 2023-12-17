import telebot
import json
import bot_utils

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

def handler(event, context):
    body = json.loads(event['body'])
    update = telebot.types.Update.de_json(body)
    bot.process_new_updates([update])

keyboard_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
science_button = telebot.types.KeyboardButton("Get Science Fact")
history_button = telebot.types.KeyboardButton("Get History Fact")
fact_of_the_day_button = telebot.types.KeyboardButton("Fact of the Day")
keyboard_markup.row(science_button, history_button)
keyboard_markup.row(fact_of_the_day_button)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Welcome! Choose an option:", reply_markup=keyboard_markup)

@bot.message_handler(func=lambda message: message.text == "Get Science Fact")
def handle_science_fact(message):
    fact = bot_utils.get_facts(topic=0)
    bot.send_message(message.chat.id, fact)

@bot.message_handler(func=lambda message: message.text == "Get History Fact")
def handle_history_fact(message):
    fact = bot_utils.get_facts(topic=1)
    bot.send_message(message.chat.id, fact)

@bot.message_handler(func=lambda message: message.text == "Fact of the Day")
def handle_fact_of_the_day(message):
    fact = bot_utils.get_facts(topic=2)
    bot.send_message(message.chat.id, fact)

bot.polling(none_stop=True)
