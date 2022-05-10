from telebot import types
from src.parser import Parser


class Helper:
    """Вспомогательный Класс для main хранит в себе функции которые используются в мейне
    
        1)Имеет методы
            buttons(Функция создаёт  кнопки на экране)
            check_is_currency_valid(Проверяет валидность введённой валюты )
            check_is_amount_valid(Проверяет валидность введённой суммы )
            
        2)Имеет параметры 
            bot(telebot)
    
    """

    def __init__(self, bot):
        self.bot = bot

    def buttons(self, prof_data):
        """Функция создаёт  кнопки на экране

            1)Имеет параметры 
                prof_data(Профиль пользователя  с его данными)

            2)Возвращаемое значение:
                markup(Наши кнопки) 
        """

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Buttons on user's messagebox.
        convert = types.KeyboardButton("convert money")
        amount = types.KeyboardButton(f"change amount")
        value_from = types.KeyboardButton(f"curency {prof_data.currency}")
        markup.add(convert, amount, value_from)  # Add buttons to markup
        return markup

    def check_is_currency_valid(self, prof_data, message):
        """Функция проверяет существует ли такой тип валюты, 
            если да то принимает его, 
            если нет то пишем заново
        
            1)Имеет параметры 
                prof_data(Профиль пользователя  с его данными)
                message(информация о сообщении от пользователя)
        
        """

        prof_data.currency = message.text.upper()
        pars = Parser()
        _ = pars.parser(prof_data)
        if _:
            markup = self.buttons(prof_data)
            self.bot.send_message(message.chat.id, f"converting value changed to {prof_data.currency}",
                                  parse_mode="html",
                                  reply_markup=markup)
            prof_data.change_value = 0
            prof_data.setinfo()
        else:
            self.bot.send_message(message.chat.id, f"Enter valid currency examples: USD,RUB,AMD,...", parse_mode="html")

    def check_is_amount_valid(self, prof_data, message):
        """Функция проверяет написали ли мы число, 
            если да то принимает его, 
            если нет то пишем заново
        
            1)Имеет параметры 
                prof_data(Профиль пользователя  с его данными)
                message(информация о сообщении от пользователя)
        """

        try:
            prof_data.amount = int(message.text)
            markup = self.buttons(prof_data)
            self.bot.send_message(message.chat.id, f"converting amount changed to {message.text}", parse_mode="html",
                                  reply_markup=markup)
            prof_data.chg_amount = 0
            prof_data.setinfo()
        except Exception:
            self.bot.send_message(message.chat.id, f"Enter valid amount type(int)", parse_mode="html")

    def keyboard_buton(self):
        """Создаёт три inline buttons
        
            1)Возвращаемое значение:
                markup(inline buttons) 
        """

        markup = types.InlineKeyboardMarkup(row_width=4)  # Buttons under previous message.
        usd = types.InlineKeyboardButton("USD", callback_data="USD")
        rub = types.InlineKeyboardButton("RUB", callback_data="RUB")
        amd = types.InlineKeyboardButton("AMD", callback_data="AMD")
        markup.add(usd, rub, amd)  # Add buttons to markup
        return markup
