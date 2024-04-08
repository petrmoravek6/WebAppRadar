import unittest
from unittest.mock import patch
import os
import json

from src.latest_version.cycle_info import CycleInfo
from src.latest_version.release_fetcher.method.github import GitHubReleaseFetcherMethod


def load_json_data(filename):
    """
    Helper function to load JSON data from a file.
    """
    path = os.path.join(os.path.dirname(__file__), 'assets', filename)
    with open(path, 'r') as file:
        return json.load(file)


class TestGitHubReleaseFetcherMethod(unittest.TestCase):

    @patch.object(GitHubReleaseFetcherMethod, '_get_json_from_api')
    def test_fetch_cycle_info_case1(self, mock_get_json):
        # Mock the _get_json_from_api to return data from your first JSON file
        mock_get_json.return_value = load_json_data('github-release-response1.json')

        expected = [
            CycleInfo('6.3', '6.3.4'),
        ]

        fetcher = GitHubReleaseFetcherMethod()
        result = fetcher.fetch_cycle_info('test', 'test', 'name', r'v(\d+\.\d+.\d+)')

        self.assertCountEqual(expected, result)

    @patch.object(GitHubReleaseFetcherMethod, '_get_json_from_api')
    def test_fetch_cycle_info_case2(self, mock_get_json):
        # Mock the _get_json_from_api to return data from your second JSON file
        mock_get_json.return_value = load_json_data('github-release-response2.json')

        expected = [
            CycleInfo('20.0', '20.0.9'),
            CycleInfo('21.1', '21.1.9'),
            CycleInfo('22.0', '22.0.3'),
            CycleInfo('23.0', '23.0.4'),
            CycleInfo('22.1', '22.1.4'),
        ]

        fetcher = GitHubReleaseFetcherMethod()
        result = fetcher.fetch_cycle_info('owner2', 'repo2', 'name', r'\S*\s*(\d+\.\d+.\d+)')

        self.assertCountEqual(expected, result)

    @patch.object(GitHubReleaseFetcherMethod, '_get_json_from_api')
    def test_fetch_cycle_info_case3(self, mock_get_json):
        # Mock the _get_json_from_api to return data from your third JSON file
        mock_get_json.return_value = load_json_data('github-release-response3.json')

        fetcher = GitHubReleaseFetcherMethod()
        result = fetcher.fetch_cycle_info('owner3', 'repo3', 'name', r'\S*\s*(\d+\.\d+.\d+)')

        self.assertCountEqual([], result)

    @patch.object(GitHubReleaseFetcherMethod, '_get_json_from_api')
    def test_fetch_cycle_info_invalid_args1(self, mock_get_json):
        """Element 'name' not present in JSON"""
        mock_get_json.return_value = [
            {
                "id": "test",
                "another_key": "test"
            }
        ]

        fetcher = GitHubReleaseFetcherMethod()
        result = fetcher.fetch_cycle_info('owner3', 'repo3', 'name', r'\S*\s*(\d+\.\d+.\d+)')

        self.assertCountEqual([], result)

    @patch.object(GitHubReleaseFetcherMethod, '_get_json_from_api')
    def test_fetch_cycle_info_invalid_args2(self, mock_get_json):
        """Element 'name' present in JSON but ver regex not present"""
        mock_get_json.return_value = [
            {
                "id": "test",
                "name": "test"
            }
        ]

        fetcher = GitHubReleaseFetcherMethod()
        result = fetcher.fetch_cycle_info('owner3', 'repo3', 'name', r'\S*\s*(\d+\.\d+.\d+)')

        self.assertCountEqual([], result)

if __name__ == '__main__':
    unittest.main()
