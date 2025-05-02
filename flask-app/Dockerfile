FROM python:3.9-slim-bullseye
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*
EXPOSE 5000
CMD ["python", "app.py"]
