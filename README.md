# WebAppRadar
This app is used for automatic network scanning for web apps deployed on Debian based machines. 
It scans given subnet or IP and returns a list of all hostnames hosted within the given network range.
However, the main feature of this app is automatic web app detection. 
For each hostname, an attempt is made to determine the name and version of the web application that is hosted by the hostname.
It then compares the information with latest releases of the app searched on the internet. 

The "final product" of this app is the comparison of the information about the current web apps running in the given network range with the latest release info for those apps.
This comparison can serve as a basic scan explore or necessary update reminder.

Please read [installation manual](INSTALL_MANUAL.md) for configure and run instructions.

See [user manual](USER_MANUAL.md) to learn how to use the application.

## DEMO
You can run WebAppRadar app in simulation environment that consists of 4 devices in isolated Docker network.
That way, you can see how the app works in small scale without installing further dependencies or scanning real network.

The demo network consists of 3 servers running Nginx or Apache2 web servers and accepting SSH connections. 
The 4th server is the app itself which performs whole network scan, web app detection and comparing the information 
with the latest web app releases using real time information.

To run the demo, use: `docker compose -f docker-compose-demo.yml up --build --exit-code-from app --abort-on-container-exit`

After all services are built and started and the scan is finished, you can see the result at the standard output.

## Testing
### Unit tests
Run `python3 -m unittest` in root folder.
### Network tests
Run `docker compose up --build --force-recreate --exit-code-from app --abort-on-container-exit` in `tests/network_tests/env<number>`