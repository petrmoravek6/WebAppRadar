# This Dockerfile represents empty apache2 server with SSH server configuration

# Use a Debian-based Apache image
FROM httpd:2.4.58-bookworm

# Install OpenSSH Server
RUN apt-get update && \
    apt-get install -y openssh-server && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir /var/run/sshd

# Add a user 'test' with the specified password
RUN useradd -m -s /bin/bash test && \
    echo 'test:test' | chpasswd

# Setup SSH to accept login with password
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Optional: Disable SSH root login
RUN sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# Permit user environment and setup PATH environment variable
RUN echo "PermitUserEnvironment yes" >> /etc/ssh/sshd_config
RUN mkdir -p /home/test/.ssh && \
    echo "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" > /home/test/.ssh/environment && \
    chown test:test /home/test/.ssh/environment && \
    chmod 600 /home/test/.ssh/environment

# Create sites-available and sites-enabled directories
RUN mkdir /usr/local/apache2/sites-available /usr/local/apache2/sites-enabled

# Include the sites-enabled directory in the main Apache configuration
RUN echo "IncludeOptional /usr/local/apache2/sites-enabled/*.conf" >> /usr/local/apache2/conf/httpd.conf

# Expose the SSH port
EXPOSE 22

# Start Apache and SSH services
CMD service ssh start && httpd-foreground
