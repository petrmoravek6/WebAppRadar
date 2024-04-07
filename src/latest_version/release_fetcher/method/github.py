import re
from packaging.version import parse
from typing import Iterable, List, Dict, Any
from src.latest_version.cycle_info import CycleInfo
import logging

from src.latest_version.release_fetcher.method.json_fetcher import JsonFetcher

logger = logging.getLogger(__name__)


class GitHubReleaseFetcherMethod(JsonFetcher):
    github_api_max_per_page = 100

    @staticmethod
    def _get_json_from_api(owner: str, repo: str, per_page: int = github_api_max_per_page) -> List[Dict[str, Any]]:
        """
        Makes a GET request to the specified API endpoint and returns the JSON response.
        """
        url = f'https://api.github.com/repos/{owner}/{repo}/releases?per_page={per_page}'
        return GitHubReleaseFetcherMethod.get_json_from_api(url)

    def fetch_cycle_info(self, repo_owner: str, repo_name: str, element: str, ver_regex: str) -> Iterable[CycleInfo]:
        """
        Processes JSON data from the API into an iterable of CycleInfo objects.
        """
        data = self._get_json_from_api(repo_owner, repo_name)
        if len(data) == 0:
            return tuple()

        cycles = dict()
        for item in data:
            try:
                ver_el = item.get(element)
                if ver_el is None:
                    logger.warning(
                        f"Couldn't find '{ver_el}' in JSON response object: {item} from '{repo_owner}/{repo_name} release API call")
                    continue
                if not isinstance(ver_el, str):
                    logger.warning(
                        f"Element '{ver_el}' in JSON response object: {item} from '{repo_owner}/{repo_name} is not a string")
                    continue
                ver_match = re.search(ver_regex, ver_el)
                if not ver_match:
                    logger.warning(
                        f"Couldn't match '{ver_regex}' in '{ver_el}' element in JSON response object: {item} from '{repo_owner}/{repo_name} release API call")
                    continue
                version = parse(ver_match.group(1))
                cycle = f'{version.major}.{version.minor}'
                if cycle not in cycles:
                    cycles[cycle] = version
                elif cycles[cycle] < version:
                    cycles[cycle] = version
            except Exception as e:
                logger.error(f"Unexpected error: {e} - Missing or wrong data in the JSON response for "
                             f"GitHub API call for '{repo_owner}/{repo_name}' app")
                continue

        if len(cycles) == 0:
            logger.error(f"Getting release info for '{repo_owner}/{repo_name} failed. "
                         f"Check previous warnings for more information.")
        return [CycleInfo(cycle, str(latest_ver)) for cycle, latest_ver in cycles.items()]
