from typing import Iterable, List, Dict, Any
from datetime import datetime
from src.latest_version.cycle_info import VersionCycleInfo
import logging

from src.latest_version.release_fetcher.method.json_fetcher import JsonFetcher
from src.latest_version.release_fetcher.method.method import IFetchMethod

logger = logging.getLogger(__name__)


class EndOfLifeReleaseFetcherMethod(JsonFetcher, IFetchMethod):

    def __init__(self, web_app_name: str, api_url: str = 'https://endoflife.date/api/'):
        self.web_app_name = web_app_name
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

    def get_all_releases(self) -> Iterable[VersionCycleInfo]:
        """
        Processes JSON data (release and EOL information about endoflife.date SW defined in the constructor) from the EndOfLife API into an iterable of VersionCycleInfo objects.
        """
        data = self._get_json_from_api(self.web_app_name)

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

                cycle_info = VersionCycleInfo(
                    cycle=cycle,
                    latest=latest,
                    eol=eol,
                    eol_date=eol_date
                )
                result.append(cycle_info)
            except Exception as e:
                logger.error(f"Unexpected error: {e} - Missing or wrong data in the JSON response for "
                             f"EndOfLife.date API call for '{self.web_app_name}' app")
                continue
        return result
