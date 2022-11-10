import csv
import os
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import Genres, Title

PATH_FILE = os.path.join('static', 'data', 'genre_title.csv')


class Command(BaseCommand):
    help = 'Загрузка жанров_произведений (genre_title) из файла'

    def handle(self, *args, **kwargs):
        with open(PATH_FILE, 'r') as file:
            data_reader = csv.reader(file)
            next(data_reader)

            for row in data_reader:
                print(row)
                title = get_object_or_404(Title, id=row[1])
                genre = get_object_or_404(Genres, id=row[2])
                title.save()
                title.genre.add(genre)
            self.stdout.write(self.style.SUCCESS('Загрузка завершена успешно'))
