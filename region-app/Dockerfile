FROM python:3.8-alpine

# Copy our requirements first because they are largely unchanging
COPY requirements.txt /
COPY requirements.docker.txt /

# Install our requirements
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev postgresql-client
RUN pip install -r /requirements.docker.txt

# Copy our source, which will be changing more frequently
COPY . /src
WORKDIR /src

# Setup the deployment
EXPOSE 8080
CMD sh -c "./await_postgres.sh && gunicorn --bind 0.0.0.0:8080 wsgi:app"
