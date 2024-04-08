import unittest
from unittest.mock import patch, MagicMock

from src.latest_version.cycle_info import CycleInfo
from src.latest_version.full_info_fetcher import FullInfoFetcher
from src.latest_version.full_web_app_info import FullWebAppInfo
from src.latest_version.semantic_version_comparator import SemanticVersionComparator
from src.latest_version.version_comparison import VersionComparison
from src.web_app_determiner.web_app_info import WebAppInfo


def custom_fetch_side_effect(web_app_name):
    if web_app_name == "App1":
        return [CycleInfo("1.0", "1.0.4", False, None)]
    elif web_app_name == "App2":
        return [CycleInfo("1.0", "1.0.3", None, None),
                CycleInfo("2.0", "2.0.1", None, None)]
    elif web_app_name == "App3":
        return [CycleInfo("1.0", "1.0.3", True, None), CycleInfo("2.0", "2.0.1", False, None),
                CycleInfo("2.1", "2.1.0", False, None)]
    return []


class TestFullInfoFetcher(unittest.TestCase):
    @patch('src.latest_version.release_fetcher.release_fetcher.ReleaseFetcher')
    def setUp(self, MockReleaseFetcher):
        self.mock_release_fetcher = MockReleaseFetcher()
        self.mock_release_fetcher.fetch_web_app_cycle_info.side_effect = custom_fetch_side_effect

        # Mock IVersionComparator for specific apps
        self.version_comparators = {
            'App1': SemanticVersionComparator(),
            'App2': SemanticVersionComparator(),
            'App4': SemanticVersionComparator()
        }

        # Instantiate FullInfoFetcher with mocked release_fetcher and semantic comparators

    def test_fetch_with_no_version(self):
        """Test the fetch method when no version is provided."""
        basic_info1 = WebAppInfo(name="App1", version=None)
        basic_info2 = WebAppInfo(name="App2", version=None)
        basic_info3 = WebAppInfo(name="App3", version=None)
        basic_info4 = WebAppInfo(name="App4", version=None)
        basic_info5 = WebAppInfo(name="App5", version=None)

        full_info_fetcher = FullInfoFetcher(
            release_fetcher=self.mock_release_fetcher,
            version_comparators=self.version_comparators,
            default_version_comparator=SemanticVersionComparator()
        )
        result1 = full_info_fetcher.fetch(basic_info1)
        result2 = full_info_fetcher.fetch(basic_info2)
        result3 = full_info_fetcher.fetch(basic_info3)
        result4 = full_info_fetcher.fetch(basic_info4)
        result5 = full_info_fetcher.fetch(basic_info5)

        self.assertEqual(result1,
                         FullWebAppInfo("App1", version=None, latest_version="1.0.4", latest_cycle_version=None,
                                        eol=None, eol_date=None))
        self.assertEqual(result2,
                         FullWebAppInfo("App2", version=None, latest_version="2.0.1", latest_cycle_version=None,
                                        eol=None, eol_date=None))
        self.assertEqual(result3,
                         FullWebAppInfo("App3", version=None, latest_version="2.1.0", latest_cycle_version=None,
                                        eol=None, eol_date=None))
        self.assertEqual(result4,
                         FullWebAppInfo("App4", version=None, latest_version=None, latest_cycle_version=None,
                                        eol=None, eol_date=None))
        self.assertEqual(result5,
                         FullWebAppInfo("App5", version=None, latest_version=None, latest_cycle_version=None,
                                        eol=None, eol_date=None))

    def test_fetch_with_versions(self):
        basic_info1 = WebAppInfo(name="App1", version='1.0.2')
        basic_info2 = WebAppInfo(name="App2", version='2.0.1')
        basic_info3 = WebAppInfo(name="App3", version='0.9.0')
        basic_info4 = WebAppInfo(name="App4", version='1.0.2')
        basic_info5 = WebAppInfo(name="App5", version='1.0.2')

        full_info_fetcher = FullInfoFetcher(
            release_fetcher=self.mock_release_fetcher,
            version_comparators=self.version_comparators,
            default_version_comparator=SemanticVersionComparator()
        )
        result1 = full_info_fetcher.fetch(basic_info1)
        result2 = full_info_fetcher.fetch(basic_info2)
        result3 = full_info_fetcher.fetch(basic_info3)
        result4 = full_info_fetcher.fetch(basic_info4)
        result5 = full_info_fetcher.fetch(basic_info5)
        
        self.assertEqual(result1,
                         FullWebAppInfo("App1", version='1.0.2', latest_version="1.0.4", latest_cycle_version="1.0.4",
                                        eol=False, eol_date=None))
        self.assertEqual(result2,
                         FullWebAppInfo("App2", version="2.0.1", latest_version="2.0.1", latest_cycle_version="2.0.1",
                                        eol=None, eol_date=None))
        self.assertEqual(result3,
                         FullWebAppInfo("App3", version='0.9.0', latest_version="2.1.0", latest_cycle_version=None,
                                        eol=None, eol_date=None))
        self.assertEqual(result4,
                         FullWebAppInfo("App4", version='1.0.2', latest_version=None, latest_cycle_version=None,
                                        eol=None, eol_date=None))
        self.assertEqual(result5,
                         FullWebAppInfo("App5", version='1.0.2', latest_version=None, latest_cycle_version=None,
                                        eol=None, eol_date=None))

    @patch('src.latest_version.semantic_version_comparator.SemanticVersionComparator')
    def test_with_default_comparator(self, MockSemanticVersionComparator):
        mock_default_version_comparator = MockSemanticVersionComparator()
        # always return this value as version comparison
        mock_default_version_comparator.get_version_comparison.return_value = VersionComparison("2.1.0", "2.1.0", True, None)
        full_info_fetcher = FullInfoFetcher(
            release_fetcher=self.mock_release_fetcher,
            version_comparators=self.version_comparators,
            default_version_comparator=mock_default_version_comparator
        )

        basic_info1 = WebAppInfo(name="App3", version='0.9.0')
        basic_info2 = WebAppInfo(name="App5", version='0.9.0')

        result1 = full_info_fetcher.fetch(basic_info1)
        result2 = full_info_fetcher.fetch(basic_info2)

        self.assertEqual(result1,
                         FullWebAppInfo("App3", version='0.9.0', latest_version="2.1.0", latest_cycle_version="2.1.0",
                                        eol=True, eol_date=None))
        # no cycle versions found for this app, so the object is expected to not compare
        self.assertEqual(result2,
                         FullWebAppInfo("App5", version='0.9.0', latest_version=None, latest_cycle_version=None,
                                        eol=None, eol_date=None))