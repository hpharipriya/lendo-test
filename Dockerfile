FROM python:3.8-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY . /app
WORKDIR /app
RUN apt-get update -y
RUN apt-get install build-essential -y
RUN apt-get install python3-dev -y
RUN pip3 install -r requirements.txt
#RUN python manage.py makemigrations

CMD [ "python", "manage.py", "makemigrations"]
CMD [ "python", "manage.py", "migrate"]
CMD [ "gunicorn", "-b", "0.0.0.0:8000", "core.wsgi"]
