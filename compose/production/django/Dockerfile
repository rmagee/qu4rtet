FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN export DOCKER=true
RUN export HTTPS_ONLY=False

RUN mkdir -p /root/.ssh
ADD ./compose/local/django/gitlab_deploy_key_rsa /root/.ssh/id_rsa
RUN chmod 700 /root/.ssh/id_rsa
RUN echo "Host gitlab.com\n\tStrictHostKeyChecking no\n" >> /root/.ssh/config

RUN addgroup --system django \
    && adduser --system django \
    && usermod -aG django django

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY ./compose/production/django/gunicorn.sh /gunicorn.sh
RUN sed -i 's/\r//' /gunicorn.sh
RUN chmod +x /gunicorn.sh
RUN chown django /gunicorn.sh

COPY ./compose/production/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN chown django /entrypoint.sh

COPY ./compose/production/django/celery/worker/start.sh /start-celeryworker.sh
RUN sed -i 's/\r//' /start-celeryworker.sh
RUN chmod +x /start-celeryworker.sh

COPY ./compose/production/django/celery/beat/start.sh /start-celerybeat.sh
RUN sed -i 's/\r//' /start-celerybeat.sh
RUN chmod +x /start-celerybeat.sh

COPY . /app
# if an env file got coppied remove it.  the
# env files should be used from the .envs folder
RUN rm /app/.env; exit 0

RUN chown -R django /app

USER django

WORKDIR /app
#VOLUME ["/app/static/", "/app/media/"]
VOLUME /static
VOLUME /media

ENTRYPOINT ["/entrypoint.sh"]
