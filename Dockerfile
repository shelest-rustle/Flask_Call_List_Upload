# Dockerfile
FROM python:3.10

# Установим рабочую директорию
WORKDIR /app

# Скопируем файл зависимостей
COPY requirements.txt .

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем остальной код приложения
COPY . .

# Установим переменную окружения
ENV FLASK_APP=main.py

# Запустим приложение
CMD ["flask", "run", "--host=0.0.0.0"]
