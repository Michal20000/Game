FROM python:3.8

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install Flask-SocketIO
RUN pip install Flask-Session
RUN pip install Flask-SqlAlchemy

COPY . .
WORKDIR .

EXPOSE 1337

USER 1000

# CMD [ "chmod", "-R", "777", "." ]
# CMD [ "chmod", "-R", "777", "./sessions" ]
CMD [ "python", "./main.py" ]
