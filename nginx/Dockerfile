FROM nginx:latest

# Update and install system programs
RUN apt-get update && apt-get install -y sudo nano

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
