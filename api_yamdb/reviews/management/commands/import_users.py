import csv
import os
from django.core.management.base import BaseCommand

from users.models import User

PATH_FILE = os.path.join('static', 'data', 'users.csv')


class Command(BaseCommand):
    help = "Загрузка пользователей (users) из файла"

    def handle(self, *args, **kwargs):
        if User.objects.exists():
            print('Данные по пользователям существуют. Удалить? Y/n')
            reply = str(input())
            if reply == 'n':
                print(
                    'Для загрузки тестовых данных, '
                    'нужно удалить существующие данные по пользователям. '
                    'Загрузка прервана!')
                return
            elif reply == 'Y':
                User.objects.all().delete()
                print('Существующие данные по пользователям были удалены')
                with open(f'{PATH_FILE}', 'r') as file:
                    data_reader = csv.reader(file)
                    next(data_reader)

                    for row in data_reader:
                        print(row)
                        User.objects.create(
                            id=row[0],
                            username=row[1],
                            email=row[2],
                            role=row[3],
                            bio=row[4],
                            first_name=row[5],
                            last_name=row[6]
                        )
                    self.stdout.write(
                        self.style.SUCCESS('Загрузка завершена успешно')
                    )
            else:
                print('Введен недопустимый вариант ответа. Загрузка прервана!')
                return

        with open(f'{PATH_FILE}', 'r') as file:
            data_reader = csv.reader(file)
            next(data_reader)

            for row in data_reader:
                print(row)
                User.objects.create(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6]
                )
            self.stdout.write(
                self.style.SUCCESS('Загрузка завершена успешно')
            )
