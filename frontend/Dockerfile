FROM python:3.9.9-slim

RUN mkdir /app
WORKDIR /app

COPY frontend/requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

#COPY . .

ADD frontend /app/frontend

ENTRYPOINT ["python3"]

CMD ["frontend/main.py"]