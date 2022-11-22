FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

<<<<<<< HEAD
COPY ./ /app
=======
COPY . .
>>>>>>> 4ca8e59e7c2310d1b82a5eb8270c69b34212331e

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]