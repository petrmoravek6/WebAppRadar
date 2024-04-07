from functools import partial
from typing import Iterable
from src.latest_version.cycle_info import CycleInfo
import logging
from src.latest_version.release_fetcher.method.endoflife import EndOfLifeReleaseFetcherMethod

logger = logging.getLogger(__name__)


class ReleaseFetcher:
    def __init__(self):
        endoflife_fetcher_method = EndOfLifeReleaseFetcherMethod()
        self.methods = {
            "Atlassian Jira": partial(endoflife_fetcher_method.fetch_cycle_info, "Atlassian Jira"),
            "Atlassian Confluence": partial(endoflife_fetcher_method.fetch_cycle_info, "Atlassian Confluence"),
            "JFrog Artifactory Pro": partial(endoflife_fetcher_method.fetch_cycle_info, "JFrog Artifactory Pro"),
            "Prometheus": partial(endoflife_fetcher_method.fetch_cycle_info, "Prometheus"),
            "Grafana": partial(endoflife_fetcher_method.fetch_cycle_info, "Grafana"),
            "GitLab": partial(endoflife_fetcher_method.fetch_cycle_info, "GitLab"),
            "Zabbix": partial(endoflife_fetcher_method.fetch_cycle_info, "Zabbix"),
            "Graylog": partial(endoflife_fetcher_method.fetch_cycle_info, "Graylog"),
            "Keycloak": partial(endoflife_fetcher_method.fetch_cycle_info, "Keycloak"),
        }

    def fetch_web_app_cycle_info(self, web_app_name: str) -> Iterable[CycleInfo]:
        if web_app_name not in self.methods:
            logger.info(f"Latest release version information could not be fetched for {web_app_name} because it is "
                        f"not supported.")
            return tuple()
        return self.methods[web_app_name]()
