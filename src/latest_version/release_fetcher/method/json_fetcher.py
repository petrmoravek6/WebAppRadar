from typing import Dict, List, Any

import requests
import logging

logger = logging.getLogger(__name__)


class JsonFetcher:
    @staticmethod
    def get_json_from_api(url: str) -> List[Dict[str, Any]]:
        """
        Makes a GET request to the specified API endpoint and returns the JSON response.
        """
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
