FROM python:3.12.4

WORKDIR /var/www

COPY /app/requirements.txt .

RUN pip install -r requirements.txt

COPY source .

CMD ["fastapi", "run", "main.py"]



