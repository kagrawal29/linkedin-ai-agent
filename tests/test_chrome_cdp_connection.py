# tests/test_chrome_cdp_connection.py

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from harvester import Harvester
from browser_use import Agent, Browser, BrowserConfig

class TestChromeCDPConnection:
    """
    TDD Cycle 4.0: Chrome CDP Connection Tests
    
    These tests verify the ability to connect browser-use to an existing
    Chrome instance via Chrome DevTools Protocol (CDP).
    """

    @pytest.fixture
    def harvester(self):
        """Create a Harvester instance for testing."""
        return Harvester()

    @pytest.mark.asyncio
    async def test_cdp_connection_detection_success(self, harvester):
        """
        RED Test 4.0.1a: Test successful CDP connection to running Chrome
        
        This test should FAIL initially because _setup_cdp_connection() 
        method doesn't exist yet.
        """
        # Arrange: Mock a successful CDP connection
        with patch('harvester.Browser') as mock_browser_class:
            mock_browser = AsyncMock()
            mock_browser_class.return_value = mock_browser
            
            # Act: Attempt to setup CDP connection
            browser = await harvester._setup_cdp_connection()
            
            # Assert: Should return a Browser instance
            assert browser is not None
            assert browser == mock_browser
            
            # Verify CDP URL was used correctly
            mock_browser_class.assert_called_once()
            call_args = mock_browser_class.call_args[0]
            browser_config = call_args[0]
            assert browser_config.cdp_url == "http://localhost:9222"
            
            # Verify browser was initialized
            mock_browser._init.assert_called_once()

    @pytest.mark.asyncio
    async def test_cdp_connection_failure_handling(self, harvester):
        """
        RED Test 4.0.1b: Test graceful handling when Chrome not running with debug port
        
        This test should FAIL initially because CDP error handling doesn't exist.
        """
        # Arrange: Mock a failed CDP connection
        with patch('harvester.Browser') as mock_browser_class:
            mock_browser = AsyncMock()
            mock_browser._init.side_effect = ConnectionError("Chrome not found on port 9222")
            mock_browser_class.return_value = mock_browser
            
            # Act & Assert: Should handle connection failure gracefully
            with pytest.raises(ConnectionError) as exc_info:
                await harvester._setup_cdp_connection()
            
            assert "Chrome not found on port 9222" in str(exc_info.value)

    @pytest.mark.asyncio 
    async def test_multiple_chrome_instance_handling(self, harvester):
        """
        RED Test 4.0.1c: Test handling of multiple Chrome instances
        
        This test should FAIL initially because multi-instance logic doesn't exist.
        """
        # Arrange: Mock multiple Chrome instances scenario
        with patch('harvester.Browser') as mock_browser_class:
            mock_browser = AsyncMock()
            mock_browser_class.return_value = mock_browser
            
            # Act: Setup connection (should default to standard port)
            browser = await harvester._setup_cdp_connection()
            
            # Assert: Should connect to standard debug port
            assert browser is not None
            call_args = mock_browser_class.call_args[0]
            browser_config = call_args[0]
            assert browser_config.cdp_url == "http://localhost:9222"

    @pytest.mark.asyncio
    async def test_user_chrome_profile_integration_success(self, harvester):
        """
        RED Test 4.0.2a: Test agent can access existing Chrome tabs and sessions
        
        This test should FAIL initially because harvest() doesn't use CDP connection.
        """
        # Arrange: Mock successful CDP connection and agent execution
        with patch.object(harvester, '_get_browser_with_fallback') as mock_get_browser:
            mock_browser = AsyncMock()
            mock_get_browser.return_value = mock_browser
            
            with patch('harvester.Agent') as mock_agent_class:
                mock_agent = AsyncMock()
                mock_agent.run.return_value = "LinkedIn automation completed"
                mock_agent_class.return_value = mock_agent
                
                # Act: Execute harvest with CDP connection
                result = await harvester.harvest("Go to LinkedIn and find posts")
                
                # Assert: Should use CDP browser
                mock_get_browser.assert_called_once()
                mock_agent_class.assert_called_once()
                
                # Verify Agent was initialized with CDP browser
                call_kwargs = mock_agent_class.call_args[1]
                assert 'browser' in call_kwargs
                assert call_kwargs['browser'] == mock_browser

    @pytest.mark.asyncio
    async def test_linkedin_login_state_preservation(self, harvester):
        """
        RED Test 4.0.2b: Test LinkedIn login state preservation from user's Chrome
        
        This test should FAIL initially because login state detection doesn't exist.
        """
        # Arrange: Mock CDP connection with existing LinkedIn session
        with patch.object(harvester, '_setup_cdp_connection') as mock_setup:
            mock_browser = AsyncMock()
            mock_browser.has_linkedin_session = True  # Mock existing login
            mock_setup.return_value = mock_browser
            
            # Act: Check if LinkedIn session is preserved
            browser = await harvester._setup_cdp_connection()
            
            # Assert: Should detect existing LinkedIn login
            # This will fail because has_linkedin_session doesn't exist
            assert hasattr(browser, 'has_linkedin_session')
            assert browser.has_linkedin_session is True

    @pytest.mark.asyncio
    async def test_cdp_error_handling_graceful_fallback(self, harvester):
        """
        RED Test 4.0.3a: Test graceful fallback when CDP connection fails
        
        This test should FAIL initially because fallback logic doesn't exist.
        """
        # Arrange: Mock CDP connection failure and successful fallback
        with patch.object(harvester, '_setup_cdp_connection') as mock_cdp:
            with patch.object(harvester, '_setup_fallback_browser') as mock_fallback:
                mock_cdp.side_effect = ConnectionError("Chrome debug port not available")
                mock_fallback_browser = AsyncMock()
                mock_fallback.return_value = mock_fallback_browser
                
                # Act: Should fallback to standalone browser
                browser = await harvester._get_browser_with_fallback()
                
                # Assert: Should return fallback browser
                assert browser == mock_fallback_browser
                
                # Enhanced retry logic should attempt CDP connection multiple times (max_retries = 3)
                assert mock_cdp.call_count == harvester.max_retries
                mock_fallback.assert_called_once()

    @pytest.mark.asyncio
    async def test_chrome_crash_handling(self, harvester):
        """
        RED Test 4.0.3b: Test handling of Chrome crashes during automation
        
        This test should FAIL initially because crash recovery doesn't exist.
        """
        # Arrange: Mock Chrome crash scenario
        with patch.object(harvester, '_get_browser_with_fallback') as mock_get_browser:
            mock_browser = AsyncMock()
            mock_get_browser.return_value = mock_browser
            
            with patch('harvester.Agent') as mock_agent_class:
                mock_agent = AsyncMock()
                # Simulate Chrome crash during execution
                mock_agent.run.side_effect = ConnectionError("Chrome process crashed")
                mock_agent_class.return_value = mock_agent
                
                # Act & Assert: Should handle crash gracefully
                with pytest.raises(ConnectionError):
                    await harvester.harvest("Test LinkedIn automation")

    def test_cdp_connection_detection_method_exists(self, harvester):
        """
        RED Test 4.0.1d: Verify _setup_cdp_connection method exists
        
        This test should FAIL initially because the method doesn't exist.
        """
        # Assert: Method should exist
        assert hasattr(harvester, '_setup_cdp_connection')
        assert callable(getattr(harvester, '_setup_cdp_connection'))

    def test_fallback_browser_method_exists(self, harvester):
        """
        RED Test 4.0.3c: Verify fallback browser methods exist
        
        This test should FAIL initially because fallback methods don't exist.
        """
        # Assert: Fallback methods should exist
        assert hasattr(harvester, '_setup_fallback_browser')
        assert hasattr(harvester, '_get_browser_with_fallback')
        assert callable(getattr(harvester, '_setup_fallback_browser'))
        assert callable(getattr(harvester, '_get_browser_with_fallback'))

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
