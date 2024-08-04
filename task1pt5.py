import argparse
import logging
from datetime import datetime, timedelta

# да, я переделала - у меня семинар совсем не грузится, написала в поддержку уже.

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

days_text = {"понедельник": 0, "вторник": 1, "среда": 2, "четверг": 3, "пятница": 4, "суббота": 5, "воскресенье": 6}
months_text = {"января": 1, "февраля": 2, "марта": 3, "апреля": 4, "мая": 5, "июня": 6, "июля": 7, "августа": 8,
               "сентября": 9, "октября": 10, "ноября": 11, "декабря": 12}


def parse_date(text):
    try:
        current_year = datetime.now().year

        parts = text.split()

        week_number = 1
        day_index = datetime.now().weekday()
        month_index = datetime.now().month

        if len(parts) == 3:
            ordinal_part = parts[0].split('-')
            week_number = int(ordinal_part[0])
            if ordinal_part[1] not in ["й", "я"]:
                raise ValueError("Неверный формат недели")

            day_of_week = parts[1]
            if day_of_week.isdigit():
                day_index = int(day_of_week) - 1
            elif day_of_week in days_text:
                day_index = days_text[day_of_week]
            else:
                raise ValueError("Неверный день недели")

            month = parts[2]
            if month.isdigit():
                month_index = int(month)
            elif month in months_text:
                month_index = months_text[month]
            else:
                raise ValueError("Неверный месяц")

        first_day_of_month = datetime(current_year, month_index, 1)
        first_day_of_month_weekday = first_day_of_month.weekday()
        days_to_add = (day_index - first_day_of_month_weekday) % 7
        first_occurrence = first_day_of_month + timedelta(days=days_to_add)
        target_date = first_occurrence + timedelta(weeks=week_number - 1)

        return target_date
    except Exception as e:
        logging.error(e)
        return None


def main():
    parser = argparse.ArgumentParser(description='Преобразование текста в дату.')
    parser.add_argument('--text', type=str, default='1-й понедельник января', help='Текст для преобразования в дату')

    args = parser.parse_args()

    date = parse_date(args.text)
    if date:
        print(date.strftime('%Y-%m-%d'))
    else:
        print("Ошибка при обработке текста")


if __name__ == "__main__":
    main()
