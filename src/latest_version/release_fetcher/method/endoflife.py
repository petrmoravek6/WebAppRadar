from typing import Iterable, List, Dict, Any
from datetime import datetime
from src.latest_version.cycle_info import CycleInfo
import logging

from src.latest_version.release_fetcher.method.json_fetcher import JsonFetcher

logger = logging.getLogger(__name__)


class EndOfLifeReleaseFetcherMethod(JsonFetcher):
    def __init__(self, api_url: str = 'https://endoflife.date/api/'):
        self.api_url = api_url

    def _get_json_from_api(self, web_app_url_name: str) -> List[Dict[str, Any]]:
        """
        Makes a GET request to the specified API endpoint and returns the JSON response.
        """
        url = f'{self.api_url}{web_app_url_name}.json'
        return EndOfLifeReleaseFetcherMethod.get_json_from_api(url)

    @staticmethod
    def _get_current_date() -> datetime.date:
        return datetime.now().date()

    def fetch_cycle_info(self, web_app_name_url: str) -> Iterable[CycleInfo]:
        """
        Processes JSON data from the API into an iterable of CycleInfo objects.
        """
        data = self._get_json_from_api(web_app_name_url)

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
                    eol = eol_date < EndOfLifeReleaseFetcherMethod._get_current_date()

                cycle_info = CycleInfo(
                    cycle=cycle,
                    latest=latest,
                    eol=eol,
                    eol_date=eol_date
                )
                result.append(cycle_info)
            except Exception as e:
                logger.error(f"Unexpected error: {e} - Missing or wrong data in the JSON response for "
                             f"EndOfLife.date API call for '{web_app_name_url}' app")
                continue
        return result
