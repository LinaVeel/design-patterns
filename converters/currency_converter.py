from abc import ABC
import time
import requests


class CurrencyConverter(ABC):
    # вместо 4 разных методов сделал 1 общий метод convert.
    # Раньше каждый класс был обязан писать чужие методы, которые ему не нужны, код был перегружен.
    # Это нарушало простой дизайн и усложняло поддержку
    def __init__(
        self,
        target_currency,
        api_url="https://api.exchangerate-api.com/v4/latest/USD",
        timeout=5,
        max_retries=3,
        retry_delay=1,
    ):
        self.target_currency = target_currency
        self.api_url = api_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.rates = self._load_rates()

    # вынесла загрузку курсов в базовый класс, чтобы не дублировать код.
    # т к одинаковый запрос к API был почти в каждом файле, это не DRY
    def _load_rates(self):
        last_error = None

        for _ in range(self.max_retries):
            try:
                response = requests.get(self.api_url, timeout=self.timeout)
                response.raise_for_status()
                data = response.json()
                return data["rates"]
            except (requests.RequestException, KeyError, ValueError) as error:
                last_error = error
                time.sleep(self.retry_delay)

        raise RuntimeError(f"Не удалось получить курсы валют: {last_error}")

    # сделан единый метод конвертации для всех валют.
    # теперь любой конкретный конвертер отличается только кодом целевой валюты, логика получения курсов и конвертации теперь в базовом классе.
    def convert(self, amount):
        if self.target_currency not in self.rates:
            raise ValueError(f"Курс для валюты {self.target_currency} не найден")
        return amount * self.rates[self.target_currency]
