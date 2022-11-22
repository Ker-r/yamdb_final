import csv
import os
from django.core.management.base import BaseCommand

from reviews.models import Genres

PATH_FILE = os.path.join('static', 'data', 'genre.csv')


class Command(BaseCommand):
    help = 'Загрузка жанров (genre) из файла'

    def handle(self, *args, **kwargs):
        if Genres.objects.exists():
            print('Данные по жанрам существуют. Удалить? Y/n')
            reply = str(input())
            if reply == 'n':
                print(
                    'Для загрузки тестовых данных, '
                    'нужно удалить существующие данные по жанрам. '
                    'Загрузка прервана!')
                return
            elif reply == 'Y':
                Genres.objects.all().delete()
                print('Существующие данные по жанрам были удалены')
                with open(PATH_FILE, 'r') as file:
                    data_reader = csv.reader(file)
                    next(data_reader)

                    for row in data_reader:
                        print(row)
                        Genres.objects.create(
                            id=row[0],
                            name=row[1],
                            slug=row[2],
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
                Genres.objects.create(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )
            self.stdout.write(
                self.style.SUCCESS('Загрузка завершена успешно')
            )
