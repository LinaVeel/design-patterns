from converters import (
    UsdRubConverter,
    UsdEurConverter,
    UsdGbpConverter,
    UsdCnyConverter,
)


def main():
    # убрала import и лишний asyncio. Т к явные импорты проще читать
    # + добавила простую обработку ошибки ввода.
    # теперь если ввести текст вместо числа, программа не падает с трассировкой, а пишет понятное сообщение
    try:
        amount = float(input("Введите значение в USD:\n"))
    except ValueError:
        print("Ошибка: нужно ввести число, например 10 или 10.5")
        return

    # сделала простой список конвертеров и единый вызов convert().
    # Чтобы код стал короче, чтобы было легче добавлять новые валюты.
    converters = [
        ("RUB", UsdRubConverter()),
        ("EUR", UsdEurConverter()),
        ("GBP", UsdGbpConverter()),
        ("CNY", UsdCnyConverter()),
    ]

    # добавила общий try/except на этап конвертации.
    # если API недоступен или курс не найден, пользователь увидит короткое понятное сообщение
    try:
        for code, converter in converters:
            print(f"{amount} USD to {code}: {converter.convert(amount)}")
    except Exception as error:
        print(f"Ошибка при конвертации: {error}")


if __name__ == "__main__":
    main()
