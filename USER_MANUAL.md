# User manual

This is a guide for configuring and using the WebAppRadar application.

## Configuration

### SSH

In order the app to be able to remotely browse servers (to read virtual host configuration), the SSH authentication has to be configured correctly.
The app tries to connect to all found devices in given network by SSH. If the server does not accept SSh connection, no info will be detected from the server.
The server has to be configured to allow a user connection. 

To configure the correct connection on the application side, user has to fill in correct information in the `config.ini` file.

There are two **authentication options** supported:

#### Private key
Set `private_key` as SSH method and fill in correct private key cipher. The path to the private key **should not be** changed unless not running the app using docker-compose (standard way), because the private key is rather mounted to the Docker container. That means the file path defined in the `config.ini` should correspond to the container's key path defined in the docker-compose file. In other words, if you don't change it there, you should not change it in the `config.ini`.

The mentioned private key will be used in all connections to all discovered servers.
```ini
[SSH]
username = user123

method = private_key
path_to_private_key_file = /app/key
private_key_cipher = RSA
```
#### Password
Set `password` as SSH method and fill in correct password which will be used in all connections to all discovered servers.
```ini
[SSH]
username = user123

method = password
password = pwd123
```
In both scenarios, the user has to provide correct username to be used to log in to the server.

If any of the necessary value is not defined correctly, the app will log the error message and terminate at the start-up.

### Docker

