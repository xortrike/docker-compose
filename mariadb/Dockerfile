FROM mariadb:latest

ENV MYSQL_ROOT_PASSWORD="1234"
ENV MYSQL_DATABASE=db_main
# ENV MYSQL_USER=admin
# ENV MYSQL_PASSWORD=12345

# Update and upgrade system
RUN apt-get update && apt-get upgrade -y

# Install
RUN apt-get install -y sudo nano

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
