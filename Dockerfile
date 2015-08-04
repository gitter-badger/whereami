FROM ubuntu:14.04
MAINTAINER yagermadden@gmail.com

RUN apt-get update && apt-get install -y \
    python \
    python-dev \
    libpq-dev \
    python-pip \
    python-psycopg2 \
    git

RUN mkdir /whereami
WORKDIR /whereami

COPY *.py /whereami/
RUN chmod +x /whereami/*.py

COPY requirements.txt /whereami/
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "whereami:app", "--log-file=-"]