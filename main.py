# Привет! Несмотря на мелкие недочеты в коде, общая логика программы верная,молодец.

# Перед сдачей работы, рекомендую прогонять код через линтеры, для соблюдения pep-8.
# Популярные линтеры:
# PyLint – https://docs.pylint.org/tutorial.html#getting-started
# Flake – https://flake8.pycqa.org/en/latest/index.html

# Хорошим тоном считается использовать аннотацию типов - помогает при разработке и чтении кода
# статья на эту тему https://habr.com/ru/company/lamoda/blog/432656/

import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # 1. Получить текущую дату, можно так – dt.date.today().
        # Это уменьшит кол-во вызываемых функций
        # 2. Также, для соблюдения общего стиля и читабельности кода,
        # определение переменной self.date можно записать так:
        # self.date = dt.date.today() if not date \
        #     else dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit

        # Рекомендую сделать данную переменную protected: self.__records = []
        # Это позволит избежать случайного изменения списка во время работы
        # программы, так как добавить новое значение можно будет только с
        # помощью функции add_record()
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0

        # По стандартам pep-8 переменные должны быть в стиле snake_case.
        # с большой буквы можно называть только классы.

        # Также, в данном случае переменная Record полностью пересекается
        # с названием одноименного класса, это может привести к ошибкам в коде,
        # Например если бы у нас была необходимость создать новый экземпляр
        # класса Record внутри цикла: new_record = Record(amount=1, comment="")
        for Record in self.records:

            # Конструкцию dt.datetime.now().date() можно вынести в отдельную
            # переменную до начала цикла, тк нет необходимости высчитывать дату
            # на каждой итерации.

            # Также, как я рекомендовал выше, можно получать сегодняшнюю дату
            # через функцию today()
            if Record.date == dt.datetime.now().date():

                # Для краткости можно воспользоваться оператором присваивания
                # total_stats += record.amount
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:

            # Данная конструкция выглядит избыточно и требует
            # времени чтобы понять ее логику, можно попробовать упростить,
            # например так (предварительно определив week_ago до начала цикла):
            # if week_ago < record.date <= today:
            #   week_stats += record.amount
            if (
                    (today - record.date).days < 7 and
                    (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):

    # Описание работы функции нужно выносить в докстринг, вместо комментария
    # https://peps.python.org/pep-0257/#one-line-docstrings
    def get_calories_remained(self):  # Получает остаток калорий на сегодня

        # Разработчик читает код гораздо чаще чем пишет, поэтому нужно
        # стараться давать такие названия переменным, которые максимально точно
        # отражают данные содержащиеся в них. Так, через некоторые время когда
        # ты снова откроешь этот код, у тебя не будет вопросов касаемо
        # содержания и назначения переменных.
        # Например: x заменить на calories_remained
        x = self.limit - self.get_today_stats()
        if x > 0:

            # Различные сообщения склонные к частому изменению или
            # повторяющийся в коде текст, лучше всего выносить в отдельные константы.
            # Если в будущем потребуется изменить содержание текста, тебе не
            # придется искать по всему коду строчки для правки.
            # Например:
            # ALLOWED_CALORIES_FOR_TODAY = f'Сегодня можно ... {calories_remained} кКал'
            # Тогда можно просто вернуть нужную константу, подставив значение:
            # return ALLOWED_CALORIES_FOR_TODAY.format(calories_remained=calories_remained)
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'

        # В данным случае стоит убрать else, оставив только return
        # логика функции никак не изменится, а читабельность улучшится
        else:
            # Круглые скобки использовать не нужно, достаточно вернуть строку
            return ('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Переменные функции, согласно pep-8, должны быть в нижнем регистре.
    # Обратил внимание, что функция называется get_today_cash_remained,
    # а в аналогичной функции класса CaloriesCalculator слова "today" в названии нет,
    # рекомендую иметь единый стиль при именовании не только переменных, но и функций/классов
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # Логика данной  конструкции верная, но она избыточная.
        # При добавлении новой валюты, придется писать очередной блок elif.
        # Подсказка:
        # Имя валюты и ее курс зависят параметра currency. Лучше создать
        # словарь со всей информацией о валютах и извлекать из него по currency
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Опечатка, = (присваивание переменной), вместо == (равенство)
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (

                # Весь текст ниже нужно вынести в константы,
                # Это заодно решит проблему с переносом строк
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'

        # Последний elif можно убрать, оставив только return.
        # В данной логике возможно три варианта значения cash_remained:
        # cash_remained > 0, cash_remained == 0, cash_remained < 0.
        # Если два из трех вариантов не прошли по условию,
        # тогда проверять третье в конструкции elif/else не нужно, тк
        # оно выполнится в любом случае
        elif cash_remained < 0:

            # Выше, для округления числа, ты использовал round(), это хорошо,
            # но давай придерживаться единого стиля при написании кода и
            # уберем {0:.2f}.

            # Так же не нужно добавлять "-" к переменной cash_remained, так как
            # по условию cash_remained < 0 она и так будет отрицательной
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    def get_week_stats(self):
        # Так как никакой дополнительной логики до/после вызова
        # родительской функции не происходит, то нет необходимости
        # переопределять эту функцию.
        # Ее можно и нужно удалить, тк работоспособность\логика программы
        # никак от этого не изменится
        super().get_week_stats()
