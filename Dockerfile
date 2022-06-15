FROM python:3.8
WORKDIR .
COPY . .
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install Flask-SocketIO
RUN pip install Flask-Session
RUN pip install Flask-SqlAlchemy
RUN chmod -R 777 .
RUN chmod -R 777 ./main.db

EXPOSE 1337
USER 1000
CMD [ "python", "./main.py" ]
