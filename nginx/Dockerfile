FROM nginx:latest

# Update and upgrade system
RUN apt-get update && apt-get upgrade -y

# Install
RUN apt-get install -y sudo nano

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
