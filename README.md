# yamdb_final
yamdb_final

[![yamdb_final workflow](https://github.com/Ker-r/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/Ker-r/yamdb_final/actions/workflows/yamdb_workflow.yml)

http://158.160.6.45/api/v1/
http://158.160.6.45/admin/

## Описание проекта 

Проект __YaMDb__ собирает _отзывы (`Review`)_ пользователей на произведения _(`Title`)_. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список _категорий (`Category`)_ может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Сами произведения в __YaMDb__ не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой _категории_ есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.
Произведению может быть присвоен _жанр (`Genre`)_ из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы _(`Review`)_ и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — _рейтинг_ (целое число). На одно произведение пользователь может оставить только один отзыв. 

### шаблон наполнения env-файла:
- DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
- DB_NAME=postgres # имя базы данных
- POSTGRES_USER=postgres # логин для подключения к базе данных
- POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
- DB_HOST=db # название сервиса (контейнера)
- DB_PORT=5432 # порт для подключения к БД

### описание команд для запуска приложения в контейнерах
- docker ps # показывает список запущенных контейнеров
- docker pull #  скачать определённый образ или набор образов
- docker build # собирает образ Docker из Dockerfile и «контекста»
- docker run # запускает контейнер, на основе указанного образа
- docker logs # команда используется для просмотра логов указанного контейнера
- docker volume ls # показывает список томов, которые являются предпочитаемым механизмом для сохранения данных, генерируемых и используемых контейнерами Docker
- docker rm # удаляет один и более контейнеров
- docker rmi # удаляет один и более образов
- docker stop # останавливает один и более контейнеров
- docker-compose up -d --build # пересборка контейнера

### описание команды для заполнения базы данными
- sudo docker-compose exec web python manage.py makemigrations reviews 
- sudo docker-compose exec web python manage.py migrate
