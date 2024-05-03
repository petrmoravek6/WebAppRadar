import unittest
from unittest.mock import patch
from datetime import datetime, date
from src.latest_version.cycle_info import VersionCycleInfo
from src.latest_version.release_fetcher.method.endoflife import EndOfLifeReleaseFetcherMethod
import logging


class TestEndOfLifeReleaseFetcherMethod(unittest.TestCase):
    def setUp(self):
        # Suppress logging below CRITICAL level
        logging.basicConfig(level=logging.CRITICAL)

    @patch.object(EndOfLifeReleaseFetcherMethod, '_get_json_from_api')
    @patch.object(EndOfLifeReleaseFetcherMethod, '_get_current_date', return_value=date(2024, 4, 7))
    def test_fetch_cycle_info_keycloak(self, mock_current_date, mock_get_json):
        # Mock response for 'keycloak'
        mock_response = [
            {"cycle": "24.0", "releaseDate": "2024-03-04", "eol": False, "latest": "24.0.2",
             "latestReleaseDate": "2024-03-24", "lts": False},
            {"cycle": "23.0", "releaseDate": "2023-11-23", "eol": "2024-05-04", "latest": "23.0.7",
             "latestReleaseDate": "2024-02-22", "lts": False},
            {"cycle": "22.0", "releaseDate": "2023-07-11", "eol": "2023-11-23", "latest": "22.0.9",
             "latestReleaseDate": "2024-03-04", "lts": False}
        ]
        mock_get_json.return_value = mock_response

        expected_results = [
            VersionCycleInfo(cycle="24.0", latest="24.0.2", eol=False, eol_date=None),
            VersionCycleInfo(cycle="23.0", latest="23.0.7", eol=False,
                             eol_date=datetime.strptime("2024-05-04", "%Y-%m-%d").date()),
            VersionCycleInfo(cycle="22.0", latest="22.0.9", eol=True,
                             eol_date=datetime.strptime("2023-11-23", "%Y-%m-%d").date()),
        ]

        fetcher = EndOfLifeReleaseFetcherMethod("Keycloak")
        actual_results = list(fetcher.get_all_releases())
        self.assertCountEqual(actual_results, expected_results)

    @patch.object(EndOfLifeReleaseFetcherMethod, '_get_json_from_api')
    @patch.object(EndOfLifeReleaseFetcherMethod, '_get_current_date', return_value=date(2024, 4, 7))
    def test_fetch_cycle_info_jira_software(self, mock_current_date, mock_get_json):
        # Mock response for 'jira-software'
        mock_response = [
            {"cycle": "8.9", "releaseDate": "2024-04-01", "eol": "2026-04-02", "latest": "8.9.0",
             "latestReleaseDate": "2024-04-01", "lts": False},
            {"cycle": "8.8", "releaseDate": "2024-02-08", "eol": "2026-02-08", "latest": "8.8.1",
             "latestReleaseDate": "2024-03-05", "lts": False},
            {"cycle": "8.7", "releaseDate": "2023-12-05", "eol": "2023-12-06", "latest": "8.7.2",
             "latestReleaseDate": "2024-01-16", "lts": True}
        ]
        mock_get_json.return_value = mock_response

        expected_results = [
            VersionCycleInfo(cycle="8.9", latest="8.9.0", eol=False,
                             eol_date=datetime.strptime("2026-04-02", "%Y-%m-%d").date()),
            VersionCycleInfo(cycle="8.8", latest="8.8.1", eol=False,
                             eol_date=datetime.strptime("2026-02-08", "%Y-%m-%d").date()),
            VersionCycleInfo(cycle="8.7", latest="8.7.2", eol=True,
                             eol_date=datetime.strptime("2023-12-06", "%Y-%m-%d").date()),
        ]

        fetcher = EndOfLifeReleaseFetcherMethod("Atlassian Jira")
        actual_results = list(fetcher.get_all_releases())

        self.assertCountEqual(actual_results, expected_results)

    def test_unsupported_web_app(self):
        fetcher = EndOfLifeReleaseFetcherMethod("UNSUPPORTED_412C841A32F6")
        self.assertCountEqual(fetcher.get_all_releases(), [])

    @patch.object(EndOfLifeReleaseFetcherMethod, '_get_json_from_api')
    def test_fetch_cycle_info_empty_response(self, mock_get_json):
        mock_response = []
        mock_get_json.return_value = mock_response

        expected_results = []

        fetcher = EndOfLifeReleaseFetcherMethod("Atlassian Jira")
        actual_results = list(fetcher.get_all_releases())

        self.assertEqual(actual_results, expected_results)
