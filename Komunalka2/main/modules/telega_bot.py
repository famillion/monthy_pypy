import telebot
import main.modules.read_write as rw

PATH_SCREEN = 'screen/shot.jpg'

PATH_BOT = 'data/tbot_data.json'

bot_data = rw.read_json(PATH_BOT)

users = set(bot_data['users'])

bot = telebot.TeleBot(bot_data['TOKEN'])


# Пілінг юзерів

# @bot.message_handler(commands=['start'])
# def mess(message):
#     users.add(message.chat.id)
#     bot.reply_to(message, "ти запілінгований! Вітаю!")
#     bot_data['users'] = list(users)
#     rw.write_to_json(PATH_BOT, bot_data)
#     print(users)
#
#
# bot.infinity_polling()

def send_to_bot():
    with open(PATH_SCREEN, 'rb') as screen:
        shot = screen.read()
        for user in users:
            bot.send_photo(user, shot)
