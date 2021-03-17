FROM mariadb:10.4

ARG TIME_ZONA

# Configure time zone
RUN ln -snf /usr/share/zoneinfo/$TIME_ZONA /etc/localtime && echo $TIME_ZONA > /etc/timezone

# Update and install system programs
RUN apt-get update && \
    apt-get install -y sudo nano

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
