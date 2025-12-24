FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
COPY db/ /app/db/

CMD ["python", "main.py"]
