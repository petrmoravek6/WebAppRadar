# Use Nginx base image
FROM nginx:stable-alpine3.17-slim

# Remove default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom Nginx configuration
COPY ./example1.conf /etc/nginx/sites-available/
RUN mkdir /etc/nginx/sites-enabled && \
    ln -s /etc/nginx/sites-available/example1.conf /etc/nginx/sites-enabled/example1.conf && \
    echo "include /etc/nginx/sites-enabled/*;" >> /etc/nginx/nginx.conf

# Copy static content
#COPY www /var/www/html

# Install OpenSSH
RUN apk add --no-cache openssh && \
    echo "root:test" | chpasswd

# Setup a user 'test' with password 'test'
RUN adduser -D test && \
    echo "test:test" | chpasswd

# Configure SSHD to accept login with password
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Generate host keys for SSHD
RUN ssh-keygen -A

# Expose SSH port
EXPOSE 22

# Start Nginx and SSH services
CMD ["/bin/sh", "-c", "exec nginx -g 'daemon off;' & /usr/sbin/sshd -D"]
