from src.latest_version.full_web_app_info import FullWebAppInfo
from src.latest_version.release_fetcher.release_fetcher import ReleaseFetcher
from src.latest_version.semantic_version_comparator import SemanticVersionComparator
from src.latest_version.verson_comparator import IVersionComparator
from src.web_app_determiner.web_app_info import WebAppInfo


class FullInfoFetcher:
    """Class used for determining all possible information about specific web app."""
    def __init__(self, release_fetcher: ReleaseFetcher, version_comparators: dict[str, IVersionComparator],
                 default_version_comparator: IVersionComparator = SemanticVersionComparator()):
        """
        Creates new instance of FullInfoFetcher
        :param release_fetcher: An instance of ReleaseFetcher used for fetching latest release information about web apps
        :param version_comparators: Dictionary of comparison methods. Each element defines a way an app version is to be compared with its another versions. Key: app name, value: fully implemented subclass of IVersionComparator
        :param default_version_comparator: default version comparator to be used if given app in 'fetch' method is not defined in 'version_comparators'
        """
        self.release_fetcher = release_fetcher
        self.version_comparators = version_comparators
        self.default_version_comparator = default_version_comparator

    def get_full_info(self, basic_info: WebAppInfo) -> FullWebAppInfo:
        """Tries to found out as much information about given web app as possible. It uses object from the constructor"""
        cycles = self.release_fetcher.fetch_web_app_cycle_info(basic_info.name)
        # no release info
        if not cycles:
            return FullWebAppInfo(basic_info.name, basic_info.version)
        if basic_info.name not in self.version_comparators:
            comparison = self.default_version_comparator.get_version_comparison(basic_info.version, cycles)
        else:
            comparison = self.version_comparators[basic_info.name].get_version_comparison(basic_info.version, cycles)
        return FullWebAppInfo(basic_info.name, basic_info.version,
                              comparison.latest_version, comparison.latest_cycle_version, comparison.eol, comparison.eol_date)