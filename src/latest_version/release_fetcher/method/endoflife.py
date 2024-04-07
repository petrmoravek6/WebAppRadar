import requests
from typing import Iterable, List, Dict, Any
from datetime import datetime
from src.latest_version.cycle_info import CycleInfo
import logging

logger = logging.getLogger(__name__)


class EndOfLifeReleaseFetcherMethod:
    def __init__(self, api_url: str = 'https://endoflife.date/api/'):
        self.api_url = api_url

    web_app_url_names = {
        "Atlassian Jira": "jira-software",
        "Atlassian Confluence": "confluence",
        "JFrog Artifactory Pro": "artifactory",
        "Prometheus": "prometheus",
        "Grafana": "grafana",
        "GitLab": "gitlab",
        "Zabbix": "zabbix",
        "Graylog": "graylog",
        "Keycloak": "keycloak",
    }

    def _get_json_from_api(self, web_app_url_name: str) -> List[Dict[str, Any]]:
        """
        Makes a GET request to the specified API endpoint and returns the JSON response.
        """
        url = f'{self.api_url}{web_app_url_name}.json'
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error during '{url}' request. {e}")
        except ValueError as e:
            logger.error(f"Value error during '{url}' request. {e} - Could not decode JSON")
        except Exception as e:
            logger.error(f"Unexpected error during '{url}' request. {e}")
        return []

    @staticmethod
    def _get_current_date() -> datetime.date:
        return datetime.now().date()

    def fetch_cycle_info(self, web_app_name: str) -> Iterable[CycleInfo]:
        """
        Processes JSON data from the API into an iterable of CycleInfo objects.
        """
        if web_app_name not in self.web_app_url_names:
            logger.error(f"Could not load latest release information for {web_app_name} using EndOfLife.date API because "
                         f"the app is not in supported list")
            return tuple()
        data = self._get_json_from_api(self.web_app_url_names[web_app_name])

        result = []
        for item in data:
            try:
                cycle = item['cycle']
                latest = item['latest']

                # Handling 'eol' which can be a boolean or a date string
                eol_raw = item['eol']
                if isinstance(eol_raw, bool):
                    eol = eol_raw
                    eol_date = None
                else:
                    eol_date = datetime.strptime(eol_raw, '%Y-%m-%d').date()
                    eol = eol_date >= EndOfLifeReleaseFetcherMethod._get_current_date()

                cycle_info = CycleInfo(
                    cycle=cycle,
                    latest=latest,
                    eol=eol,
                    eol_date=eol_date
                )
                result.append(cycle_info)
            except Exception as e:
                logger.error(f"Unexpected error: {e} - Missing or wrong data in the JSON response for "
                             f"EndOfLife.date API call for {web_app_name} app")
                continue
        return result
