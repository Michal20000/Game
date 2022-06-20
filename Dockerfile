FROM python:3.8
WORKDIR /game
COPY . .
COPY requirements.txt .
VOLUME /game/databases
EXPOSE 1337

RUN pip install -r requirements.txt
RUN chmod 777 ./databases
RUN chmod 777 ./databases/main.db
USER 1000
ENTRYPOINT [ "python", "./main.py" ]
