import datetime as dt
from decimal import Decimal
from typing import (Optional, NoReturn, List, Literal, Dict)


# Будут использованы префиксы из статьи: https://habr.com/ru/post/473308/

class Record:
    """Информация о трате"""

    def __init__(self, amount: Decimal, comment: str, date: Optional[str] = None) -> NoReturn:
        self.amount: Decimal = amount
        if date is None:  # расскрываем условие полностью для более легкого восприятия и читаемости
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment = comment


class BaseCalculator:
    """Базовый класс для реализации основных функций калькулятора"""

    def __init__(self, limit: Decimal) -> NoReturn:
        # type hinting-и помогают при разработке
        self.limit: Decimal = limit
        self.records: List[Record] = []

    def add_record(self, record: Record) -> NoReturn:
        """Метод для фиксирования записи о расходе"""
        self.records.append(record)

    def get_today_stats(self) -> Decimal:
        """Метод для определния потрачаннех средств за сегодняшний день"""
        today_stats: Decimal = Decimal()
        # создаем отдельную переменную, чтобы не вычислять ее при каждой итерации
        today = dt.datetime.now().date()
        for record in self.records:
            if record.date == today:
                today_stats += record.amount
        return today_stats

    def get_week_stats(self) -> Decimal:
        """Метод для определения размера потраченных средств за неделю"""
        week_stats: Decimal = Decimal()
        today = dt.datetime.now().date()
        for record in self.records:
            # находиться ли дата в интервале текущй недели
            if 7 > (today - record.date).days >= 0:
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(BaseCalculator):
    """Калькулятор калорий"""  # nit: В  docstring краткое описание класса

    def get_calories_remained(self) -> Decimal:
        """Метод для получения остатка калорий на сегодня"""
        return self.limit - self.get_today_stats()

    def get_calories_remained_display(self) -> str:
        # выносим логику получения остатка калорий в отдельный
        # метод для дальнейшего использования и раделения отвественности
        calories_remained: Decimal = self.get_calories_remained()
        if calories_remained:
            return (
                f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью '
                f'не более {calories_remained} кКал'
            )
        return 'Хватит есть!'


class CashCalculator(BaseCalculator):
    """Калькулятор денежных средств"""
    USD_RATE: Decimal = Decimal(60)  # Курс доллар США.
    EURO_RATE: Decimal = Decimal(70)  # Курс Евро.
    RUB_RATE: Decimal = Decimal(65)  # Курс рубля

    def __init__(
            self,
            *args,
            rub_rate: Optional[Decimal] = None,
            euro_rate: Optional[Decimal] = None,
            usd_rate: Optional[Decimal] = None,
            **kwargs
    ) -> NoReturn:
        # из вне могут передать аргументы, иначе используем атрибуты класса

        # используем Decimal для корректной работы с числами
        self.usd_rate: Optional[Decimal] = usd_rate or self.USD_RATE
        self.euro_rate: Optional[Decimal] = euro_rate or self.EURO_RATE
        self.rub_rate: Optional[Decimal] = rub_rate or self.RUB_RATE
        # работаем только с теми переменными, которые будут использоваться в текущем классе,
        # остальные аргументы отдаем родителю
        super().__init__(*args, **kwargs)

    def get_today_cash_remained(self, currency_type: Literal['usd', 'eur', 'rub']) -> Dict[str, Decimal]:
        """
        Метод для оперделения количество денежных средств,
        которых можно потратить за сегодняшний день
        """
        cash_remained: Decimal = self.limit - self.get_today_stats()
        # проверяем, пришел ли нам известный тип
        if currency_type == 'usd':
            return {'USD': cash_remained / self.usd_rate}
        elif currency_type == 'eur':
            return {'Euro': cash_remained / self.euro_rate}
        elif currency_type == 'rub':
            return {'руб': cash_remained / self.rub_rate}
        # если пришел неизвестный тип, то уведомляем внешних пользователей
        raise ValueError('Неизвестный тип валюты')


__all__ = ('CaloriesCalculator', 'CashCalculator',)
