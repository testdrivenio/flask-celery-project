FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Additional dependencies
  && apt-get install -y telnet netcat \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN addgroup --system flask \
    && adduser --system --ingroup flask flask

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./compose/production/flask/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint
RUN chown flask /entrypoint

COPY ./compose/production/flask/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown flask /start

COPY ./compose/production/flask/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker
RUN chown flask /start-celeryworker

COPY ./compose/production/flask/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat
RUN chown flask /start-celerybeat

COPY ./compose/production/flask/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

RUN mkdir /app
RUN mkdir /app/upload
RUN mkdir /app/flower_db
WORKDIR /app

# copy project code
COPY . .

RUN chown -R flask:flask /app

USER flask

ENTRYPOINT ["/entrypoint"]
