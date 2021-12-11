FROM python:3.9-alpine

# Recommended when running python in docker, tells python to run unbuffered to avoid future complication 
ENV PYTHONUNBUFFERED 1 

# requirements.tsxt will be used to store our dependencies, below line tells to copy from left file to docker image in said file
COPY ./requirements.txt /requirements.txt

# tells to install all dependencies from requirements.txt 
RUN pip install -r /requirements.txt

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