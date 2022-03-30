FROM python:3.9.9-slim
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY frontend/requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

#COPY . .

ADD frontend /app/frontend

ENTRYPOINT ["python"]
CMD ["frontend/main.py", "-u"]