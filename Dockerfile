FROM python:3.8
WORKDIR /game
COPY . .
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN chmod 777 ./databases
RUN chmod 777 ./databases/main.db

VOLUME /game/databases
EXPOSE 1337
USER 1000
ENTRYPOINT [ "python", "./main.py" ]
