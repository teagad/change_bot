#!/usr/bin/env python3
import os
import telebot
from src.parser import Parser
from src.data import Player_data
from src.helper import Helper

# Создаем экземпляр бота
bot = telebot.TeleBot(os.environ["BOT_TOKEN"])


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(msg):
    """Начала игры, при вводе команды start выводит письмо приветствия"""

    prof_data = Player_data(msg.from_user.first_name)
    prof_data.standart_value()
    bot.send_message(msg.chat.id, f"Welcome, <i>{msg.from_user.first_name}</i>!\n" +
                     f"My name is <b>{bot.get_me().first_name}</b> and my purpose to show "
                     f"the convertation.", parse_mode="html")
    bot.send_message(msg.chat.id, "For future work with this telegram bot, please choose an option", parse_mode="html")
    bot.send_message(msg.chat.id,
                     "1)to start the conversion process click exchange in menu\n\n"
                     "2)to display the exchange rate one to one, click course in menu",
                     parse_mode="html")


@bot.message_handler(commands=["help"])
def help(msg):
    """Документация к боту при вводе команды help, помощь пользователям"""

    bot.send_message(msg.chat.id, f"Welcome, <i>{msg.from_user.first_name}</i>!\n" +
                     f"My name is <b>{bot.get_me().first_name}</b> and my purpose to show "
                     f"the convertation.", parse_mode="html")
    bot.send_message(msg.chat.id, "For future work with this telegram bot, please choose an option", parse_mode="html")
    bot.send_message(msg.chat.id,
                     "what can i do?\n"
                     "1)to start the conversion process click exchange in menu\n\n"
                     "2)to display the exchange rate one to one, click course in menu",
                     parse_mode="html")
    bot.send_message(msg.chat.id,
                     "exchange\n"
                     "1)to set the amount and currency of the transfer, "
                     "you need to click on the change amount button and set the transfer amount\n\n "
                     "2) click on the curency and set the currency from which we transfer\n\n "
                     "3) click on convert money and select which currency we transfer to.",
                     parse_mode="html")


@bot.message_handler(commands=["exchange"])
def exchange(msg):
    """При команде exchange выводит правила пользования и создаёт кнопки"""

    prof_data = Player_data(msg.from_user.first_name)
    helper = Helper(bot)
    markup = helper.buttons(prof_data)
    bot.send_message(msg.chat.id,
                     "1)to set the amount and currency of the transfer, "
                     "you need to click on the change amount button and set the transfer amount\n\n "
                     "2) click on the curency and set the currency from which we transfer\n\n "
                     "3) click on convert money and select which currency we transfer to.",
                     parse_mode="html",
                     reply_markup=markup)


@bot.message_handler(commands=["cours"])
def course(msg):
    """При команде course выводит курс некоторых зарубежных валют в рублях"""

    file_photo = open("asserts/transfer.jpg", 'rb')
    bot.send_photo(chat_id=msg.from_user.id, photo=file_photo)
    prof_data = Player_data(msg.from_user.first_name)
    pars = Parser()
    text = ""
    usd_course = pars.parser(prof_data, "USD")
    text += f"1 RUB is {usd_course}\n\n"
    eur_course = pars.parser(prof_data, "EUR")
    text += f"1 RUB is {eur_course}\n\n"
    amd_course = pars.parser(prof_data, "AMD")
    text += f"1 RUB is {amd_course}"
    bot.send_message(msg.chat.id, text, parse_mode="html")


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    """Реализация кнопок которые были созданы сверху"""

    prof_data = Player_data(message.from_user.first_name)
    helper = Helper(bot)

    if message.text == "convert money":
        markup = helper.keyboard_buton()
        bot.send_message(message.chat.id, 'choose the value to convert', parse_mode="html",
                         reply_markup=markup)

    elif message.text == f"change amount":
        bot.send_message(message.chat.id, f"Enter the amount you want to exchange. "
                                          f"Now it is: <b>{prof_data.amount}{prof_data.currency}</b>",
                         parse_mode="html")
        prof_data.chg_amount = 1  # Option 'Change home city' was chosen.
        prof_data.setinfo()

    elif message.text == f"curency {prof_data.currency}":
        bot.send_message(message.chat.id, f"Enter the value you want to exchange from. "
                                          f"Now it is: <b>{prof_data.currency}</b>", parse_mode="html")
        prof_data.change_value = 1  # Option 'Change home city' was chosen.
        prof_data.setinfo()

    elif prof_data.change_value:
        helper.check_is_currency_valid(prof_data, message)

    elif prof_data.chg_amount:
        helper.check_is_amount_valid(prof_data, message)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """
    Реализация inline buttons которые были созданы при нажати кнопки в верхней функции
    """

    try:
        prof_data = Player_data(call.message.chat.first_name)
        if call.message:
            if call.data in ["USD", "RUB", "AMD"]:
                pars = Parser()
                text = pars.parser(prof_data, call.data)
                bot.send_message(call.message.chat.id, f'{prof_data.amount} {prof_data.currency} is ' + text,
                                 parse_mode="html")
    except Exception as e:
        bot.send_message(call.message.chat.id, 'not valid value to change ',
                         parse_mode="html")
        print(repr(e))


bot.polling(none_stop=True)  # Launch bot.
