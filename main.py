# Общие замечания
# 1. Перед всеми классами необходимо оставлять 2 пустые строки
# 2. Все классы должны иметь docsting(строки с описанием класса): начинаются с большой буквы, заканчиваются точкой и содержат описание того, что делает функция. Google -> Docstring Conventions
# 3. Перед всеми методами необходимо оставлять 1 пустую строку
# 4. Пропущены пробелы вокруг операторов: =
# 5. Длина строки — 79 символов
# Ты уже умеешь пользоваться pip, поэтому воспользуйся им и установи pep8(pip install pep). Запустив его(pep8 main.py) можно увидеть список нарушений PEP8
import datetime as dt
# неиспользуемая библиотека
import json

# Хорошо бы добавить в класс метод __str__ или __repr__ чтобы иметь строковое представление объекта. Если возможно, должен возвращать строку, по которой можно воссоздать тот же самый объект. В противном случае, строку вида <...описание объекта...>.
class Record:
    # date = None
    # Классно было бы добавить type hintings 
    def __init__(self, amount, comment, date=''):
        # amount - денежная сумма или количество килокалорий, поэтому лучше воспользоваться Decimal(from decimal import Decimal), он обеспечит точность при подсчетах
        self.amount=amount
        self.date = dt.datetime.now().date() if not date else dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment=comment
class Calculator:
    # переменную limit лучше переименовать в day_limit, так как в задании установлен именно дневной лимит
    def __init__(self, limit):
        self.limit = limit
        self.records=[]
    # аргумент record должен принимать объект класса Record, в текущем виде можно добавить что угодно, хорошо бы хотя бы type hinting'ом указать требуемое, а в идеале проверить что полученное соотвествует ожидаемому
    def add_record(self, record):
        self.records.append(record)
    def get_today_stats(self):
        today_stats=0
        # название переменной лучше с маленькой
        for Record in self.records:
            # запрашивать каждый раз дату в цикле долго, лучше запросить ее вне цикла и использовать ее
            if Record.date == dt.datetime.now().date():
                # PEP8 принято так: today_stats += Record.amount + неоднороденое использование кода
                today_stats = today_stats+Record.amount
        return today_stats
    def get_week_stats(self):
        week_stats=0
        today = dt.datetime.now().date()
        for record in self.records:
            # вычислать дельту 1 раз и потом сравнивать меньше по количеству операций
            if (today -  record.date).days <7 and (today -  record.date).days >=0:
                week_stats +=record.amount
        return week_stats
class CaloriesCalculator(Calculator):
    # Плохой комментарий, но хороший docsting.
    def get_calories_remained(self): # Получает остаток калорий на сегодня
        # Название переменной должно быть более говорящим, например rest_cal
        x=self.limit-self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {x} кКал'
        else:
            return 'Хватит есть!'
class CashCalculator(Calculator):
    # Decimal даст большую точность, ведь точность Денег это важно!
    USD_RATE=float(60) #Курс доллар США.
    EURO_RATE=float(70) #Курс Евро.
    # метод на вход принимает только код валюты, поэтому USR_RATE лучше использовать через self
    def get_today_cash_remained(self, currency, USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type=currency
        cash_remained = self.limit - self.get_today_stats()
        # лучше создать словарь с требуемыми именами: {'usd': 'USD'}, это избавит от большого количества условий(благодаря циклу) и облегчит добавление новых валют в будущем. Еще надо обработать ошибку при остутсвии валюты
        if currency=='usd':
            cash_remained /= USD_RATE
            currency_type ='USD'
        elif currency_type=='eur':
            cash_remained /= EURO_RATE
            currency_type ='Euro'
        elif currency_type=='rub':
            # магическая переменная
            cash_remained == 1.00
            currency_type ='руб'
        if cash_remained > 0:
            # В f-строках применяется только подстановка переменных и нет логических или арифметических операций, вызовов функций и подобной динамики.
            # Чтобы округлить с помощью Decimal: number.quantize(Decimal('1.00')) или смотри другие методы в документации
            return f'На сегодня осталось {round(cash_remained, 2)} {currency_type}'
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            return 'Денег нет, держись: твой долг - {0:.2f} {1}'.format(-cash_remained, currency_type)

    # переопределение функции. благодаря наследованию можно просто воспользоваться self.get_week_stats(), а текущий метод полностью удалить.
    def get_week_stats(self):
        super().get_week_stats()
