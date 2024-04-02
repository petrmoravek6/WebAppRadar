# Use Nginx base image
FROM nginx:1.24-bullseye

# Remove default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom Nginx configuration
COPY ./example1.conf /etc/nginx/sites-available/
RUN mkdir /etc/nginx/sites-enabled && \
    ln -s /etc/nginx/sites-available/example1.conf /etc/nginx/sites-enabled/example1.conf && \
    echo "include /etc/nginx/sites-enabled/*;" >> /etc/nginx/nginx.conf

# Copy static content
#COPY www /var/www/html

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

# Expose the SSH port
EXPOSE 22

# Start Nginx and SSH services
CMD service ssh start && nginx -g 'daemon off;'
