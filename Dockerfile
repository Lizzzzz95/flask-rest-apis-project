FROM python:3.11
# EXPOSE 5000
# Removed above line as gunicorn will be exposed on port 80
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
# CMD ["flask", "run", "--host", "0.0.0.0"]
# Removed above line in place of gunicorn command
CMD [ "gunicorn", "--bind", "0.0.0.0:80", "app:create_app()" ]