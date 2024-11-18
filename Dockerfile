FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev-compat \
    libmariadb-dev
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]