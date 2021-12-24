FROM docker:latest

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV APP_DIR /app

RUN mkdir ${APP_DIR}
WORKDIR ${APP_DIR}

RUN apk add --update python3 py-pip apk-cron && rm -rf /var/cache/apk/*

ADD ./app/requirements.txt .
RUN pip3 install --ignore-installed six && pip3 install -r requirements.txt
COPY ./app .

RUN /usr/bin/crontab ./crontab.txt