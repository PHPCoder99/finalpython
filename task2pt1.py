import csv
import json
import random
import logging
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def save_to_json(func):
    def wrapper(*args):
        result_list = []
        try:
            with open(args[0], 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    try:
                        a, b, c = map(int, row)
                        logging.info(f'Чтение строки: {row}')
                        result = func(a, b, c)
                        data = {'parameters': [a, b, c], 'result': result}
                        result_list.append(data)
                    except ValueError as e:
                        logging.error(f'Ошибка конвертации значений строки {row} в int: {e}')
                    except Exception as e:
                        logging.error(f'Ошибка при обработке строки {row}: {e}')
            with open('results.json', 'w') as f:
                json.dump(result_list, f)
            logging.info('Результаты успешно сохранены в results.json')
        except FileNotFoundError as e:
            logging.error(f'Файл {args[0]} не найден: {e}')
        except Exception as e:
            logging.error(f'Ошибка при работе с файлом {args[0]}: {e}')

    return wrapper


@save_to_json
def find_roots(a, b, c):
    try:
        d = b ** 2 - 4 * a * c
        if d < 0:
            logging.info(f'Дискриминант отрицательный ({d}), корней нет')
            return None
        elif d == 0:
            logging.info(f'Дискриминант равен нулю ({d}), один корень')
            return -b / (2 * a)
        else:
            x1 = (-b + d ** 0.5) / (2 * a)
            x2 = (-b - d ** 0.5) / (2 * a)
            logging.info(f'Два корня: x1 = {x1}, x2 = {x2}')
            return x1, x2
    except Exception as e:
        logging.error(f'Ошибка при нахождении корней квадратного уравнения: {e}')
        return None


def generate_csv_file(file_name, rows):
    try:
        with open(file_name, 'w', newline='') as f:
            writer = csv.writer(f)
            for i in range(rows):
                row = [random.randint(1, 1000) for _ in range(3)]
                writer.writerow(row)
        logging.info(f'CSV файл {file_name} успешно создан с {rows} строками')
    except Exception as e:
        logging.error(f'Ошибка при создании CSV файла {file_name}: {e}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Обработка CSV файла для нахождения корней квадратных уравнений и сохранение результатов в JSON.')
    parser.add_argument('csv_file', type=str, help='Путь к CSV файлу с коэффициентами квадратных уравнений')
    parser.add_argument('--generate', type=int, help='Создать CSV файл с указанным количеством строк')
    args = parser.parse_args()

    if args.generate:
        generate_csv_file(args.csv_file, args.generate)
    else:
        find_roots(args.csv_file)
