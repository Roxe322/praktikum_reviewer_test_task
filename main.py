from datetime import datetime as dt


class Record:
    """- Комментарий"""
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = dt.now().date() if not date else dt.strptime(date, '%d.%m.%Y').date()
        self.comment = comment


class Calculator:
    """- Комментарий"""
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """- Комментарий"""
        self.records.append(record)

    def get_today_stats(self):
        """- Комментарий"""
        today_stats = 0

        for record in self.records:
            if record.date == dt.now().date():
                today_stats += record.amount

        return today_stats

    def get_week_stats(self):
        """- Комментарий"""
        week_stats = 0
        today = dt.now().date()

        for record in self.records:
            if 7 > (today - record.date).days >= 0:
                week_stats += record.amount

        return week_stats


class CaloriesCalculator(Calculator):
    """- Комментарий"""
    def get_calories_remained(self):
        """- Получает остаток калорий на сегодня"""
        x = self.limit - self.get_today_stats()

        if x > 0:
            return f'''
            Сегодня можно съесть что-нибудь ещё,
            но с общей калорийностью не более {x} кКал'''

        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    """- Комментарий"""
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # def get_today_cash_remained(self, currency):
    def get_today_cash_remained(self, currency, usd_rate=USD_RATE, euro_rate=EURO_RATE):
        """- Комментарий"""
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()

        if currency == 'usd':
            cash_remained /= usd_rate
            currency_type = 'USD'

        elif currency_type == 'eur':
            cash_remained /= euro_rate
            currency_type = 'Euro'

        elif currency_type == 'rub':
            cash_remained = 1.00
            currency_type = 'Руб'

        if cash_remained > 0:
            result = round(cash_remained, 2)
            return f'''
            На сегодня осталось {result} 
            {currency_type}'''

        elif cash_remained == 0:
            return 'Денег нет, но вы держитесь ;)'

        elif cash_remained < 0:
            return f'''
            Денег нет, но вы держитесь ;) : 
            твой долг - {-cash_remained:.2f} {currency_type}'''

    def get_week_stats(self):
        """- Комментарий"""
        super().get_week_stats()
