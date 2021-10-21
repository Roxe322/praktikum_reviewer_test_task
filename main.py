import datetime as date_time   # dt ambiguous namig
# import json Неиспользованный import
# нет документов
# добавить 2 новые строки между imports и классами


class Record:
    # добавить новую строку между методами и классом

    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.comment = comment
        self.date = date

    @property
    def amount(self):   # включить проверку значения или сделать свою логику
        '''
            get amount
        '''
        return self._amount

    @amount.setter
    def amount(self, value):
        '''
            set amount
        '''
        self._amount = value

    @property
    def date(self):
        '''
            get date
        '''
        return self._date

    @date.setter
    def date(self, date):
        '''
            set date
        '''
        _date = date_time.datetime.now()
        if date:
            _date = _date.strptime(date, '%d.%m.%Y')

        self._date = _date.date()

    @property
    def comment(self):   # включить проверку значения или сделать свою логику
        '''
            get comment
        '''
        return self._comment

    @comment.setter
    def comment(self, value):
        '''
            set comment
        '''
        self._comment = value


class RecordContainer:

    '''
     контейнер для всех records Single responsibility (Soild)
    '''
    def __init__(self, limit):
        self.limit = limit
        self.records = []  # добавление пробелов вокруг оператора (=)

    def add_record(self, amount, comment, date=''):
        self.records.append(Record(amount=amount, comment=comment, date=date))


# между каждым классом должно быть 2 новых строки
class Calculator(RecordContainer):
    # добавить новую строку между методами и классом

    # между каждым методом должна быть новая строка
    def get_today_stats(self):
        '''
         Считать сколько денег потрачено сегодня
        '''
        today_stats = 0  # добавление пробелов вокруг оператора (=)
        for record in self.records:
            if record.date == date_time.datetime.now().date():
                today_stats = today_stats + record.amount
        return today_stats

    def get_week_stats(self):   # между каждым методом должна быть новая строка
        '''
         Считать сколько калорий получено за последние 7 дней
        '''
        week_stats = 0  # добавление пробелов вокруг оператора (=)
        today = date_time.datetime.now().date()
        for record in self.records:
            # уменьшить строку до менее 80 символов
            # удалить несколько пробелов после оператора (-)
            # пробелы после (> =) или (<)
            # используя DRY (Не повторяйся)
            days = (today - record.date).days
            if days < 7 and days >= 0:
                # добавление пробела после оператора (+ =)
                week_stats += record.amount
        return week_stats


# между каждым классом должно быть 2 новых строки
class CaloriesCalculator(Calculator):

    # удалить ненужный комментарий
    def get_calories_remained(self):
        # добавление пробелов вокруг оператора (=) и (-)
        answer = 'Хватит есть!'
        x = self.limit - self.get_today_stats()
        if x > 0:
            # уменьшить строку до менее 80 символов
            answer_text_1 = 'Сегодня можно съесть что-нибудь ещё'
            answer_text = f'{answer_text_1}, но с общей калорийностью не более'
            answer = f'{answer_text} {x} кКал'
            return answer
        return answer


class CurrencyRates:

    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.


# между каждым классом должно быть 2 новых строки
class CashCalculator(Calculator):

    def get_today_cash_remained(
        self,
        currency
    ):
        '''
         Возвращает он сообщение о состоянии дневного баланса в этой валюте
         округляя сумму до двух знаков после запятой
        '''
        cash_remained = self.limit - self.get_today_stats()
        currency = Currency(currency, cash_remained)
        cash_remained = currency.cash_remained
        currency_type = currency.currency_type

        response = Response(cash_remained, currency_type)
        return response.data


class EuroCurrency:
    def __init__(self, cash_remained) -> None:
        self.cash_remained = cash_remained

    @property
    def cash_remained(self):
        return self._cash_remained

    @cash_remained.setter
    def cash_remained(self, value):
        self._cash_remained = value

    def calc_cash_remained(self):
        self.cash_remained /= CurrencyRates.EURO_RATE
        return self.cash_remained

    def type(self):
        return "Euro"


class RubCurrency:
    def __init__(self, cash_remained) -> None:
        self.cash_remained = cash_remained

    @property
    def cash_remained(self):
        return self._cash_remained

    @cash_remained.setter
    def cash_remained(self, value):
        self._cash_remained = value

    def calc_cash_remained(self):
        return self.cash_remained

    def type(self):
        return "руб"


class USDCurrency:
    def __init__(self, cash_remained) -> None:
        self.cash_remained = cash_remained

    @property
    def cash_remained(self):
        return self._cash_remained

    @cash_remained.setter
    def cash_remained(self, value):
        self._cash_remained = value

    def calc_cash_remained(self):
        self.cash_remained /= CurrencyRates.USD_RATE
        return self.cash_remained

    def type(self):
        return "USD"


class Currencies:
    '''
     доступных валют
    '''
    HOOKS = {
        'usd': USDCurrency,
        'eur': EuroCurrency,
        'rub': RubCurrency,
    }


class Currency:
    '''
     основная логика для всех валют
    '''
    def __init__(self, currency, cash_remained) -> None:
        self.run(currency, cash_remained)

    def run(self, currency, cash_remained):
        currency = currency.lower().strip()
        currency = self.get_currency(currency)
        currency = currency(cash_remained)
        self.cash_remained = currency.calc_cash_remained()
        self.currency_type = currency.type()

    def get_currency(self, currency):
        try:
            currency = Currencies.HOOKS[currency]
        except:
            print('we don\'t have this currency yet')
            exit()
        return currency

    @property
    def cash_remained(self):
        return self._cash_remained

    @cash_remained.setter
    def cash_remained(self, value):
        self._cash_remained = value

    @property
    def currency_type(self):
        return self._currency_type

    @currency_type.setter
    def currency_type(self, value):
        self._currency_type = value


class Response:
    '''
        возвращает response для пользователя
    '''
    def __init__(self, cash_remained, currency_type) -> None:
        self.handle_response(cash_remained, currency_type)

    def handle_response(self, cash_remained, currency_type):
        if cash_remained > 0:
            text_part = 'На сегодня осталось '
            self.data = f'{text_part}{round(cash_remained, 2)} {currency_type}'
        elif cash_remained == 0:
            self.data = 'Денег нет, держись'
        else:
            answer_text = 'Денег нет, держись: твой долг -'
            self.data = '{answer_text} {0:.2f} {1}'.format(
                - cash_remained,
                currency_type
            )
