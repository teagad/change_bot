import pickle


class Player_data:
    """Класс создан для взаимодействия с хранилищем данных для получения данных о пользователе"""

    def __init__(self, profile):
        self.amount = 0
        self.currency = 0
        self.profile = profile
        self.change_value = 0
        self.chg_amount = 0
        self.getinfo()

    def getinfo(self):
        """ считавания данных Пользователя С хранилище данных"""

        try:
            with open('data.pickle', 'rb') as f:
                dic = pickle.load(f)
                profile_data = dic[self.profile]
                self.amount = int(profile_data[0])
                self.currency = profile_data[1]
                self.change_value = int(profile_data[2])
                self.chg_amount = int(profile_data[3])

        except Exception:
            standart_amount = 1
            standart_currency = "RUB"
            self.amount = standart_amount
            self.currency = standart_currency
            self.change_value = 0
            self.chg_amount = 0

    def setinfo(self):
        """запись данных Пользователя в хранилище"""

        try:
            with open('data.pickle', 'rb') as f:
                dic = pickle.load(f)
                dic[self.profile] = [
                    str(self.amount),
                    str(self.currency),
                    str(self.change_value),
                    str(self.chg_amount)
                ]
            with open('data.pickle', 'wb') as f:
                pickle.dump(dic, f)

        except Exception:
            dic = {self.profile: [
                str(self.amount),
                str(self.currency),
                str(self.change_value),
                str(self.chg_amount)
            ]}
            with open('data.pickle', 'wb') as f:
                pickle.dump(dic, f)

    def standart_value(self):
        """Выставления стандартных аргументов для пользователя"""

        standart_amount = 1
        standart_currency = "RUB"
        self.amount = standart_amount
        self.currency = standart_currency
        self.change_value = 0
        self.chg_amount = 0
        self.setinfo()
