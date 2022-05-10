import requests
from bs4 import BeautifulSoup as BS


class Parser:
    """Класс создан для взаимодействия с сайтом и получения оттуда информации
    
    1)Имеет методы
        parser(Конвертация валют при помощи сайта,отправка запроса на сайт)
        build_url(Составление ссылки)
    
    """

    def parser(self, profile, courency_to_convert="RUB"):
        """Конвертация валют при помощи сайта,отправка запроса на сайт

            Параметры: 
                profile: Профиль пользователя  с его данными 
                courency_to_convert: Валюта в которую переводим С дефолт значением RUB
        
            Возвращаемое значение:
                Возвращает Результат конвертации

        """

        r = requests.get(self.build_url(profile, courency_to_convert))
        html = BS(r.content, 'html.parser')

        for el in html.select(".result__BigRate-sc-1bsijpp-1"):
            return str(el.text)

    def build_url(self, profile, courency_to_convert):
        """Составление ссылки

            Параметры: 
                profile: Профиль пользователя  с его данными
                courency_to_convert: Валюта в которую переводим        

            Возвращаемое значение:
                Возвращает сгенерированную ссылку
        """

        return f"https://www.xe.com/currencyconverter/convert/?Amount={profile.amount}&From={profile.currency}&To={courency_to_convert}"
