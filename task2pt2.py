import csv
import logging
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Student:
    def __init__(self, name, subjects_file):
        try:
            self.name = name
            self.subjects = {}
            self.load_subjects(subjects_file)
            logging.info(f'Студент {self.name} успешно создан.')
        except Exception as e:
            logging.error(f'Ошибка при создании студента: {e}')
            raise

    def __setattr__(self, name, value):
        if name == 'name':
            if not value.replace(' ', '').isalpha() or not value.istitle():
                logging.error("ФИО должно состоять только из букв и начинаться с заглавной буквы")
                raise ValueError("ФИО должно состоять только из букв и начинаться с заглавной буквы")
        super().__setattr__(name, value)

    def __getattr__(self, name):
        if name in self.subjects:
            return self.subjects[name]
        else:
            logging.error(f"Предмет {name} не найден")
            raise AttributeError(f"Предмет {name} не найден")

    def __str__(self):
        return f"Студент: {self.name}\nПредметы: {', '.join(self.subjects.keys())}"

    def load_subjects(self, subjects_file):
        try:
            with open(subjects_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    subject = row[0]
                    if subject not in self.subjects:
                        self.subjects[subject] = {'grades': [], 'test_scores': []}
            logging.info(f'Предметы успешно загружены из {subjects_file}.')
        except FileNotFoundError as e:
            logging.error(f'Файл {subjects_file} не найден: {e}')
            raise
        except Exception as e:
            logging.error(f'Ошибка при загрузке предметов из {subjects_file}: {e}')
            raise

    def add_grade(self, subject, grade):
        try:
            if subject not in self.subjects:
                self.subjects[subject] = {'grades': [], 'test_scores': []}
            if not isinstance(grade, int) or grade < 2 or grade > 5:
                logging.error("Оценка должна быть целым числом от 2 до 5")
                raise ValueError("Оценка должна быть целым числом от 2 до 5")
            self.subjects[subject]['grades'].append(grade)
            logging.info(f'Оценка {grade} добавлена по предмету {subject}.')
        except Exception as e:
            logging.error(f'Ошибка при добавлении оценки: {e}')
            raise

    def add_test_score(self, subject, test_score):
        try:
            if subject not in self.subjects:
                self.subjects[subject] = {'grades': [], 'test_scores': []}
            if not isinstance(test_score, int) or test_score < 0 or test_score > 100:
                logging.error("Результат теста должен быть целым числом от 0 до 100")
                raise ValueError("Результат теста должен быть целым числом от 0 до 100")
            self.subjects[subject]['test_scores'].append(test_score)
            logging.info(f'Результат теста {test_score} добавлен по предмету {subject}.')
        except Exception as e:
            logging.error(f'Ошибка при добавлении результата теста: {e}')
            raise

    def get_average_test_score(self, subject):
        try:
            if subject not in self.subjects:
                logging.error(f"Предмет {subject} не найден")
                raise ValueError(f"Предмет {subject} не найден")
            test_scores = self.subjects[subject]['test_scores']
            if len(test_scores) == 0:
                return 0
            average = sum(test_scores) / len(test_scores)
            logging.info(f'Средний результат тестов по предмету {subject}: {average}')
            return average
        except Exception as e:
            logging.error(f'Ошибка при вычислении среднего результата тестов: {e}')
            raise

    def get_average_grade(self):
        try:
            total_grades = []
            for subject in self.subjects:
                grades = self.subjects[subject]['grades']
                if len(grades) > 0:
                    total_grades.extend(grades)
            if len(total_grades) == 0:
                return 0
            average = sum(total_grades) / len(total_grades)
            logging.info(f'Средняя оценка по всем предметам: {average}')
            return average
        except Exception as e:
            logging.error(f'Ошибка при вычислении средней оценки: {e}')
            raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Работа с данными студента.')
    parser.add_argument('name', type=str, help='Имя студента')
    parser.add_argument('subjects_file', type=str, help='Путь к файлу с предметами')
    parser.add_argument('--add_grade', nargs=2, metavar=('subject', 'grade'), help='Добавить оценку по предмету')
    parser.add_argument('--add_test_score', nargs=2, metavar=('subject', 'test_score'),
                        help='Добавить результат теста по предмету')
    parser.add_argument('--get_average_test_score', metavar='subject',
                        help='Получить средний результат тестов по предмету')
    parser.add_argument('--get_average_grade', action='store_true', help='Получить среднюю оценку по всем предметам')

    args = parser.parse_args()

    student = Student(args.name, args.subjects_file)

    if args.add_grade:
        subject, grade = args.add_grade
        student.add_grade(subject, int(grade))

    if args.add_test_score:
        subject, test_score = args.add_test_score
        student.add_test_score(subject, int(test_score))

    if args.get_average_test_score:
        average_test_score = student.get_average_test_score(args.get_average_test_score)
        print(f'Средний результат тестов по предмету {args.get_average_test_score}: {average_test_score}')

    if args.get_average_grade:
        average_grade = student.get_average_grade()
        print(f'Средняя оценка по всем предметам: {average_grade}')
