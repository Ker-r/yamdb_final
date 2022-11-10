import csv
import os
from django.core.management.base import BaseCommand

from reviews.models import Title, Categories

PATH_FILE = os.path.join('static', 'data', 'titles.csv')


class Command(BaseCommand):
    help = "Загрузка произведений (titles) из файла"

    def handle(self, *args, **kwargs):
        if Title.objects.exists():
            print('Данные по произведениям существуют. Удалить? Y/n')
            reply = str(input())
            if reply == 'n':
                print(
                    'Для загрузки тестовых данных, '
                    'нужно удалить существующие данные по произведениям. '
                    'Загрузка прервана!')
                return
            elif reply == 'Y':
                Title.objects.all().delete()
                print('Существующие данные по произведениям были удалены')
                with open(PATH_FILE, 'r') as file:
                    data_reader = csv.reader(file)
                    next(data_reader)

                    for row in data_reader:
                        print(row)
                        Title.objects.create(
                            id=row[0],
                            name=row[1],
                            year=row[2],
                            category=Categories(pk=row[3])
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
                Title.objects.create(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category=Categories(pk=row[3])
                )
            self.stdout.write(
                self.style.SUCCESS('Загрузка завершена успешно')
            )
