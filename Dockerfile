FROM python:3.9.6

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app
COPY . .

# Install and setup poetry
RUN pip install -r requirements.txt

WORKDIR /usr/src/app/starlink

ENV FLASK_APP=coordinates_api
ENV FLASK_DEBUG=1

ENTRYPOINT ["/bin/sh", "-c" , "python3 transform_data.py && flask run -h 0.0.0.0 -p 80"]
