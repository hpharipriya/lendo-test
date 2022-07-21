FROM python:3.8-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY . /app
WORKDIR /app
RUN apt-get update -y
RUN apt-get install build-essential -y
RUN apt-get install python3-dev -y
RUN pip3 install -r requirements.txt
CMD ["python", "worker.py"]