import unittest
from unittest.mock import patch
import os
import json
from your_module_path.github_release_fetcher_method import GitHubReleaseFetcherMethod  # Adjust the import path


class TestGitHubReleaseFetcherMethod(unittest.TestCase):

    def load_json_data(self, filename):
        """
        Helper method to load JSON data from a file.
        """
        path = os.path.join(os.path.dirname(__file__), 'assets', filename)
        with open(path, 'r') as file:
            return json.load(file)

    @patch.object(GitHubReleaseFetcherMethod, '_get_json_from_api')
    def test_fetch_cycle_info_case1(self, mock_get_json):
        # Mock the _get_json_from_api to return data from your first JSON file
        mock_get_json.return_value = self.load_json_data('github-release-response1.json')

        fetcher = GitHubReleaseFetcherMethod()
        result = fetcher.fetch_cycle_info('owner1', 'repo1', 'element1', r'ver_regex1')

        # Your testing logic here

    @patch.object(GitHubReleaseFetcherMethod, '_get_json_from_api')
    def test_fetch_cycle_info_case2(self, mock_get_json):
        # Mock the _get_json_from_api to return data from your second JSON file
        mock_get_json.return_value = self.load_json_data('github-release-response2.json')

        fetcher = GitHubReleaseFetcherMethod()
        result = fetcher.fetch_cycle_info('owner2', 'repo2', 'element2', r'ver_regex2')

        # Your testing logic here

    @patch.object(GitHubReleaseFetcherMethod, '_get_json_from_api')
    def test_fetch_cycle_info_case3(self, mock_get_json):
        # Mock the _get_json_from_api to return data from your third JSON file
        mock_get_json.return_value = self.load_json_data('github-release-response3.json')

        fetcher = GitHubReleaseFetcherMethod()
        result = fetcher.fetch_cycle_info('owner3', 'repo3', 'element3', r'ver_regex3')

        # Your testing logic here


if __name__ == '__main__':
    unittest.main()
