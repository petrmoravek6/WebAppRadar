# WebAppRadar

## Testing
### Unit tests
Run `python3 -m unittest` in root folder.
### Network tests
Run `docker compose up --build --force-recreate --remove-orphans --exit-code-from app --abort-on-container-exit` in `tests/network_tests/env<number>`.