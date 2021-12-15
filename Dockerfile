FROM python:3.9-alpine

# Recommended when running python in docker, tells python to run unbuffered to avoid future complication 
ENV PYTHONUNBUFFERED 1 

# requirements.tsxt will be used to store our dependencies, below line tells to copy from left file to docker image in said file
COPY ./requirements.txt /requirements.txt

# needed for "psycopg2" to work with docker
    # apk => package mnanager that comes with alpine 
    # add => Add Package 
    # --update => update the registry before adding 
    # --no-cache => dont store the registry index on docker file
RUN apk add --update --no-cache postgresql-client

# Install the temp dependancies which will be removed after requirement installed 
    # --virtual : sets up an alias for dependecies, so that we can remove those dependencies later
RUN apk add --update --no-cache --virtual .tmp-build-dev \
        gcc libc-dev linux-headers postgresql-dev

# tells to install all dependencies from requirements.txt 
RUN pip install -r /requirements.txt

# deleting temp dependancies 
RUN apk del .tmp-build-dev

# creates a directory named app
RUN mkdir /app 
# sets wor directory as app in docker image
WORKDIR /app
# copies content from source code to docker image 
COPY ./app /app

# creates a user, -D => creastes user to run the app/ process/ project, if we create a user 
# to run the app it provides security to the app, if we dont do that project will be run using root account(default)
RUN adduser -D user
# sets default user
USER user