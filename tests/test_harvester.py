import pytest
from unittest.mock import patch, MagicMock

# This import will fail initially, which is expected for the RED step.
from harvester import Harvester

def test_harvester_initialization_and_login(mocker):
    """
    RED: Tests that the Harvester class initializes and calls the necessary
    Playwright methods to launch a browser and log in.
    """
    # 1. Setup: Mock the entire Playwright sync_api context
    mock_playwright_context = MagicMock()
    mock_browser = MagicMock()
    mock_page = MagicMock()

    # Arrange the mock returns
    mocker.patch('playwright.sync_api.sync_playwright', return_value=mock_playwright_context)
    mock_playwright_context.__enter__.return_value.chromium.launch.return_value = mock_browser
    mock_browser.new_page.return_value = mock_page

    # 2. Execution: Instantiate the Harvester
    harvester = Harvester()
    harvester.login()

    # 3. Assertion: Verify that the key methods were called
    mock_playwright_context.__enter__.return_value.chromium.launch.assert_called_once_with(headless=False)
    mock_browser.new_page.assert_called_once()
    mock_page.goto.assert_called_once_with("https://www.linkedin.com/feed/")
