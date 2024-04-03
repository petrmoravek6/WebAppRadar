# Use a Debian-based Nginx image
FROM nginx:1.24-bullseye

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

# Copy the Nginx site configuration to sites-available and create a symlink in sites-enabled
RUN mkdir -p /etc/nginx/sites-available /etc/nginx/sites-enabled
COPY example1.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/example1.conf /etc/nginx/sites-enabled/

COPY nginx.conf /etc/nginx/nginx.conf

# Copy the HTML content
COPY dummy_index.html /var/www/html

# Expose the SSH port
EXPOSE 22

# Start Nginx and SSH services
CMD service ssh start && nginx -g 'daemon off;'
