# Installation manual

This is a guide for configuring and running the WebAppRadar application. The application runs in isolated Docker environment along with MongoDB database.
Application provides HTTP API endpoints for integrating with users.

## Prerequisites
Mandatory requirements of the application:
- internet connection
- Docker installed
- all servers you want to scan have to have SSH connection enabled (see SSH section)
- the SSH user that is to be used during SSH connection does not require sudo privilege (it only needs READ permissions to _/etc/nginx_ and _/etc/apache2_ configuration files and permission to _systemctl/service status_ command)

## Configuration

### SSH

In order the app to be able to remotely browse servers (to read virtual host configuration), the SSH authentication has to be configured correctly.
The app tries to connect to all found devices in given network by SSH. If the server does not accept SSH connection, 
no info will be detected from the server. 

To configure the correct connection on the application side, you have to fill in correct information in the `config.ini` file.

There are two **authentication options** supported:

#### Private key
Set `private_key` as SSH method and fill in correct private key cipher. 

The path to the private key **should not be** changed unless not running the app using docker-compose (standard way), because the private key is rather mounted to the Docker container. That means the file path defined in the `config.ini` should correspond to the container's key path defined in the docker-compose file. In other words, if you don't change it there, you should not change it in the `config.ini`.

The mentioned private key will be used in all connections to all discovered servers.
```ini
[SSH]
username = user123

method = private_key
path_to_private_key_file = /app/key
private_key_cipher = RSA
```
#### Password
Set `password` as SSH auth method and fill in correct password which will be used in all connections to all discovered servers.
```ini
[SSH]
username = user123

method = password
password = pwd123
```
In both scenarios, you have to provide correct username to be used to log in to the server.

If any of the necessary value is not defined correctly, the app will log the error message and terminate at the start-up.

### Docker

The application runs in isolated Docker environment. Before running the application, you can set following configuration:

#### Change API port

To change the port that is used for HTTP API connections on the local machine, please add following lines to `docker-compose.yml`:
```
command: ["-p", "<port_number>"]
```
so the complete file can look something like this:
```yaml
services:
  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"

  app:
    build:
      context: .
      dockerfile: Dockerfile
    network_mode: host
    environment:
      - MONGO_URI=mongodb://localhost:27017/
    volumes:
      - ${PWD}/config.ini:/app/config.ini
      - /home/john/.ssh/id_rsa:/app/key
    depends_on:
      - mongodb
    command: ["-p", "8080"]

```

#### Change SSH private key path
If you chose to use private key method ass SSH authentication, you have to adjust to correct file path to the key on the local machine in `docker-compose.yml`.
Set the correct path instead of `/home/john/.ssh/id_rsa`.

### Extending the list of supported web applications

You can change the list (`web-apps.json`) the app is using for determining the current name and version of the web application.

In order to determine these pieces of information, the app visits all the found hostnames via headless HTTP browser. It reads the whole page content and looks for specific HTML element parts.
If the element part is found using regular expressions, the app matches the given hostname with the name of the application.

Similar principle is used for searching the version of the web app. Another regexp with parameter is used for searching the current version of the web app from the HTML page content.

Here is an example for `Grafana` web application defined in `web-apps.json`:
```json
{
    "name": "Grafana",
    "identifier": "<title>Grafana</title>",
    "version": "a href=\"\\S+\" target=\"_blank\" rel=\"noopener noreferrer\" id=\"version\">v(\\d+\\.\\d+\\.\\d+)"
}
```
During web app determination phase, WebAppRadar visits a hostname using headless browser, renders client side JavaScript and gets the whole content page.
Then it looks for all `identifier` values and tries to match them with the page content. If `<title>Grafana</title>`
is found on the page, now we know _Grafana_ is running under the hostname.

WebAppRadar then tries to extract a version from the page by using `version` as parametrized regexp. If the parameter is matched, now we also found the current version of Grafana.

Sometimes versions are not present on the main page and they are hidden behind login. User can provide `username` and `password`
that will be used to get behind the auth wall. However, the WebAppRadar needs to know where the username and password input boxes are located on the page in order to successfully submit the values.

```json
{
  "name": "GitLab",
  "identifier": "<meta content=\"GitLab\" property=\"og:site_name\">",
  "auth": {
    "method": "username_and_password",
    "user_box_params": [
      {
        "key": "name",
        "value": "username"
      }
    ],
    "pwd_box_params": [
      {
        "key": "name",
        "value": "password"
      }
    ],
    "username": "user123",
    "password": "password123"
  },
  "version": "gon.version=\"(\\d+\\.\\d+\\.\\d+)\";"
}
```

Here we can see that apart from `identifier` and `version` values, WebAppRadar needs to know the user HTML input box element has HTML attribute
 `name` with value `username` and the password input box has `name` attribute with `password` value. The `username` and `password` are then
filled in to those input boxes and submitted using ENTER. **Only after successful authentication a version is to be read** unlike 
the case where the authentication part is not specified and the version is read directly from the main page.

**Identifier is always being matched from the main page.**

Regardless of whether the authentication method is used or not, sometimes the version does not appear immediately on the page.

You can define a relative path to the hostname that is to be used for searching the `version`. 
```json
{
    "name": "Prometheus",
    "identifier": "<title>Prometheus</title>",
    "version_path": "/status",
    "version": "<th scope=\"row\">Version</th>\\s*<td>(\\d+\\.\\d+\\.\\d+)</td>"
}
```
Web application information discovery process if the web app is `Prometheus`:
1. Hostname _example.com_ main page is completely loaded using headless browser.
2. `<title>Prometheus</title>` is found on the page.
3. `example.com/status` is loaded.
4. `<th scope=\"row\">Version</th>\\s*<td>(\\d+\\.\\d+\\.\\d+)</td>` is found on the page and the version is extracted using the regexp parameter.

Another example that combines version path with authentication (also on separate path):
```json
{
    "name": "Keycloak",
    "identifier": "<title>Welcome to Keycloak</title>",
    "auth":{
      "auth_path": "/admin/master/console/",
      "method": "username_and_password",
      "user_box_params": [
        {"key": "id", "value": "username"}
      ],
      "pwd_box_params": [
        {"key": "id", "value": "password"}
      ],
      "username": "user123",
      "password": "password123"
    },
    "version_path": "/status",
    "version": "<div class=\"version\">(\\d+\\.\\d+\\.\\d+)</div>"
  }
```
Web application information discovery process if the web app is `Keycloak`:
1. Hostname _example2.com_ main page is completely loaded using headless browser.
2. `<title>Welcome to Keycloak</title>` is found on the page.
3. `example.com/admin/master/console/` is loaded.
4. Input box with HTML attribute `id=username` is found
5. Input box with HTML attribute `id=password` is found
6. `user123` and `password` are filled in those input boxes and submitted
7. `/status` is appended to current URL and the page is loaded.
8. `<div class=\"version\">(\\d+\\.\\d+\\.\\d+)</div>` is found on the page and the version is extracted using the regexp parameter.


**If any step fails, only the previously found facts are returned.**

You can adjust the `web-apps.json` or add other web app rules. Restart the WebAppRadar app to propagate the changes.

NOTE: There is currently no support for defining additional web apps releases. WebAppRadar currently only compares the current web app info
with latest releases of predefined list of web apps, that cannot be changed in a form of configuration file.

## Running the app

After successful configuration you can run the app using `docker compose up --build` or `docker compose up --build -d` in detached mode.

## Logging

The app uses logging mechanism that implicitly logs all DEBUG, INFO, WARNING and ERROR logs to `app.log` inside the Docker container and
INFO, WARNING and ERROR logs to the console. This can be adjusted in `app.py`.
