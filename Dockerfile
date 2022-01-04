FROM python:3.10.0

WORKDIR /app
COPY . /app

RUN mkdir -p /app/logs \
    && cd /app \
    && pip3 install --no-cache-dir pipenv \
    && pipenv install --system --deploy --ignore-pipfile


ENV FLASK_ENV=production
ENV FLASK_APP manage.py
ENV FLASK_RUN_PORT=8080
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_DEBUG=0


EXPOSE 8080

CMD ["flask", "run"]
