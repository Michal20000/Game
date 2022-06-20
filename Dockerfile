FROM python:3.8
WORKDIR /game
COPY . .
COPY requirements.txt .
EXPOSE 1337
VOLUME /game/databases

RUN pip install -r requirements.txt
RUN chmod 777 ./databases
RUN chmod 777 ./databases/main.db
ENTRYPOINT [ "python", "./main.py" ]
