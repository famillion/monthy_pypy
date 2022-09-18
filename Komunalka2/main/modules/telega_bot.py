import telebot

PATH_SCREEN = 'screen/shot.jpg'

users = []

bot = telebot.TeleBot()

# @bot.message_handler(commands=['start'])
# def mess(message):
#     users.add(message.chat.id)
#     print(users)
#     bot.reply_to(message, "ти запілінгований! Вітаю!")
#
# bot.polling()


def send_to_bot():
    with open(PATH_SCREEN, 'rb') as screen:
        shot = screen.read()
        for user in users:
            bot.send_photo(user, shot)
