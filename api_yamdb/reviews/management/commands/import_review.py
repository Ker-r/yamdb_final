import csv
import os
from django.core.management.base import BaseCommand

from reviews.models import Review
from users.models import User

PATH_FILE = os.path.join('static', 'data', 'review.csv')


class Command(BaseCommand):
    help = "Загрузка отзывов (review) из файла"

    def handle(self, *args, **kwargs):
        if Review.objects.exists():
            print('Данные по отзывам существуют. Удалить? Y/n')
            reply = str(input())
            if reply == 'n':
                print(
                    'Для загрузки тестовых данных, '
                    'нужно удалить существующие данные по отзывам. '
                    'Загрузка прервана!')
                return
            elif reply == 'Y':
                Review.objects.all().delete()
                print('Существующие данные по отзывам были удалены')
                with open(PATH_FILE, 'r') as file:
                    data_reader = csv.reader(file)
                    next(data_reader)

                    for row in data_reader:
                        print(row)
                        Review.objects.create(
                            id=row[0],
                            title_id=row[1],
                            text=row[2],
                            author=User(id=row[3]),
                            score=row[4],
                            pub_date=row[5]
                        )
                    self.stdout.write(
                        self.style.SUCCESS('Загрузка завершена успешно')
                    )
            else:
                print('Введен недопустимый вариант ответа. Загрузка прервана!')
                return

        with open(PATH_FILE, 'r') as file:
            data_reader = csv.reader(file)
            next(data_reader)

            for row in data_reader:
                print(row)
                Review.objects.create(
                    id=row[0],
                    title_id=row[1],
                    text=row[2],
                    author=User(id=row[3]),
                    score=row[4],
                    pub_date=row[5]
                )
            self.stdout.write(
                self.style.SUCCESS('Загрузка завершена успешно')
            )
