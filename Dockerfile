FROM python:3.12.1-alpine3.19

WORKDIR /bot

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV SERVER_PORT=8080

CMD ["sh", "-c", "exec python3 main.py"]
