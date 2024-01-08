
FROM python:3.10

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

# Install postgres client
# RUN apk add --update --no-cache postgresql-client

# create root directory for our project in the container
RUN mkdir /SharmaAcademy

# Set the working directory to /SharmaAcademy
WORKDIR /SharmaAcademy

# Copy the current directory contents into the container at /SharmaAcademy
ADD . /SharmaAcademy/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt


# sudo systemctl status redis
# sudo systemctl stop redis
# sudo systemctl restart redis
# sudo docker compose up --build
# docker exec -it b9b0d07da754 env