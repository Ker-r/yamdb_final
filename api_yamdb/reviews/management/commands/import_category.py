import csv
import os
from django.core.management.base import BaseCommand

from reviews.models import Categories


PATH_FILE = os.path.join('static', 'data', 'category.csv')


class Command(BaseCommand):
    help = 'Загрузка категорий (category) из файла'

    def handle(self, *args, **kwargs):
        if Categories.objects.exists():
            print('Данные по категориям существуют. Удалить? Y/n')
            reply = str(input())
            if reply == 'n':
                print(
                    'Для загрузки тестовых данных, '
                    'нужно удалить существующие данные по категориям. '
                    'Загрузка прервана!')
                return
            elif reply == 'Y':
                Categories.objects.all().delete()
                print('Существующие данные по категориям были удалены')
                with open(PATH_FILE, 'r') as file:
                    data_reader = csv.reader(file)
                    next(data_reader)

                    for row in data_reader:
                        print(row)

                        Categories.objects.create(
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

                Categories.objects.create(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )
            self.stdout.write(
                self.style.SUCCESS('Загрузка завершена успешно')
            )
