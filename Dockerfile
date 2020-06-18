FROM python:3.6
WORKDIR /app

ENV APPLICATION_PORT 8000

ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

ADD . /app
ENTRYPOINT ["/app/entrypoint.sh"]