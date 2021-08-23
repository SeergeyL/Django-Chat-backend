FROM python:3.9

RUN mkdir -p /app
WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD python /app/manage.py makemigrations
CMD python /app/manage.py migrate
CMD python /app/manage.py runserver 0:8000