FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY MyAPP .

CMD ["gunicorn", "MyAPP.wsgi:application", "--bind", "0.0.0.0:8000"]