import csv
import os
from django.core.management.base import BaseCommand

from reviews.models import Comment
from users.models import User

PATH_FILE = os.path.join('static', 'data', 'comments.csv')


class Command(BaseCommand):
    help = 'Загрузка комментариев (comments) из файла'

    def handle(self, *args, **kwargs):
        if Comment.objects.exists():
            print('Данные по комментариям существуют. Удалить? Y/n')
            reply = str(input())
            if reply == 'n':
                print(
                    'Для загрузки тестовых данных, '
                    'нужно удалить существующие данные по комментариям. '
                    'Загрузка прервана!')
                return
            elif reply == 'Y':
                Comment.objects.all().delete()
                print('Существующие данные по комментариям были удалены')
                with open(PATH_FILE, 'r') as file:
                    data_reader = csv.reader(file)
                    next(data_reader)

                    for row in data_reader:
                        print(row)
                        Comment.objects.create(
                            id=row[0],
                            review_id=row[1],
                            text=row[2],
                            author=User(id=row[3]),
                            pub_date=row[4]
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
                Comment.objects.create(
                    id=row[0],
                    review_id=row[1],
                    text=row[2],
                    author=User(id=row[3]),
                    pub_date=row[4]
                )
            self.stdout.write(
                self.style.SUCCESS('Загрузка завершена успешно')
            )
