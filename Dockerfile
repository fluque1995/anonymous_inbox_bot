FROM python:3.8-slim
WORKDIR /app
ENV PYTHONUNBUFFERED True
COPY *.txt .
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt
COPY . ./

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
