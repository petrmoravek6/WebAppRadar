from functools import partial
from typing import Iterable, Dict
from src.latest_version.cycle_info import CycleInfo
import logging

logger = logging.getLogger(__name__)


class ReleaseFetcher:
    def __init__(self, methods: Dict[str, partial]):
        self.methods = methods
        # endoflife_fetcher_method = EndOfLifeReleaseFetcherMethod()
        # github_fetcher_method = GitHubReleaseFetcherMethod()
        #
        # self.methods = {
        #     "Atlassian Jira": partial(endoflife_fetcher_method.fetch_cycle_info, "jira-software"),
        #     "Atlassian Confluence": partial(endoflife_fetcher_method.fetch_cycle_info, "confluence"),
        #     "JFrog Artifactory Pro": partial(endoflife_fetcher_method.fetch_cycle_info, "artifactory"),
        #     "Prometheus": partial(endoflife_fetcher_method.fetch_cycle_info, "prometheus"),
        #     "Grafana": partial(endoflife_fetcher_method.fetch_cycle_info, "grafana"),
        #     "GitLab": partial(endoflife_fetcher_method.fetch_cycle_info, "gitlab"),
        #     "Zabbix": partial(endoflife_fetcher_method.fetch_cycle_info, "zabbix"),
        #     "Graylog": partial(endoflife_fetcher_method.fetch_cycle_info, "graylog"),
        #     "Keycloak": partial(endoflife_fetcher_method.fetch_cycle_info, "keycloak"),
        #     "Bareos": partial(github_fetcher_method.fetch_cycle_info, 'bareos', 'bareos', "name", r'\S*\s*(\d+\.\d+.\d+)'),
        #     "Snipe-IT": partial(github_fetcher_method.fetch_cycle_info, 'snipe', 'snipe-it', "name", r'v(\d+\.\d+.\d+)')
        # }

    def fetch_web_app_cycle_info(self, web_app_name: str) -> Iterable[CycleInfo]:
        if web_app_name not in self.methods:
            logger.info(f"Latest release version information could not be fetched for {web_app_name} because it is "
                        f"not supported.")
            return tuple()
        return self.methods[web_app_name]()
