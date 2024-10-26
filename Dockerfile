
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py run_websockets & python manage.py runserver 0.0.0.0:8000"]
