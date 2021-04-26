FROM python:3-alpine AS Base
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM Base as Build
WORKDIR /app
COPY . .
EXPOSE 8080
ENTRYPOINT ["python3", "flask-mysql-api.py"]