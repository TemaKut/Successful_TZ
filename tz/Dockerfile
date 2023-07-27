FROM python:3.11-slim 

WORKDIR /app/

COPY ./requirements.txt ./

RUN python -m pip install --upgrade pip

RUN pip3 install -r ./requirements.txt --no-cache-dir

COPY ../ ./

RUN python manage.py makemigrations && python manage.py migrate

CMD python manage.py runserver 0:8000