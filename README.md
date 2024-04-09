# WebAppRadar

## DEMO
You can run WebAppRadar app in simulation environment that consists of 4 devices in isolated Docker network.
That way, you can see how the app works in small scale without installing further dependencies or scanning real network.

The demo network consists of 3 servers running Nginx or Apache2 web servers and accepting SSH connections. 
The 4th server is the app itself which performs whole network scan, web app detection and comparing the information 
with the latest web app releases using real time information.

To run the demo, use: `docker compose -f docker-compose-demo.yml up --build --force-recreate --exit-code-from app --abort-on-container-exit`

After all services are built and started and the scan is finished, you can see the result at the standard output.

## Testing
### Unit tests
Run `python3 -m unittest` in root folder.
### Network tests
Run `docker compose up --build --force-recreate --exit-code-from app --abort-on-container-exit` in `tests/network_tests/env<1/2/3>`