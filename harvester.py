# harvester.py

import asyncio
import os
import logging
from pathlib import Path
from browser_use import Agent, Browser, BrowserConfig
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from models import FetchedPost
from typing import Union, List, Optional, Any

load_dotenv()

# Configure logging for CDP operations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
Harvester module for executing LinkedIn tasks via browser automation.

This module has been simplified to accept natural language prompts directly
and pass them to browser-use Agent, eliminating the need for command parsing.

Enhanced with Chrome CDP persistent login support for session reuse.
"""

class CDPConnectionError(Exception):
    """Specific exception for Chrome DevTools Protocol connection issues."""
    pass

class ChromeNotRunningError(CDPConnectionError):
    """Chrome is not running with remote debugging enabled."""
    pass

class ChromeConnectionTimeoutError(CDPConnectionError):
    """Timeout while connecting to Chrome CDP."""
    pass

class Harvester:
    """
    Simplified harvester that executes natural language prompts on LinkedIn.
    
    Replaces the complex command-based approach with direct prompt passing
    to browser-use Agent for maximum flexibility.
    
    Enhanced with Chrome CDP connection for persistent LinkedIn sessions.
    """
    
    def __init__(self):
        """Initialize the Harvester with an LLM and CDP configuration."""
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        
        # Set up browser data directory for future persistence
        self.browser_data_dir = Path.home() / ".linkedin_ai_agent" / "browser_data"
        self.browser_data_dir.mkdir(parents=True, exist_ok=True)
        
        # CDP connection settings
        self.cdp_url = "http://localhost:9222"
        self.connection_timeout = 10  # seconds
        self.max_retries = 3
        
        # Connection state tracking
        self._last_browser_instance = None
        self._connection_healthy = False
    
    async def _check_chrome_availability(self) -> bool:
        """
        Check if Chrome is running with remote debugging enabled.
        
        Returns:
            True if Chrome CDP is available, False otherwise
        """
        try:
            # Try to import aiohttp, fallback to basic check if not available
            try:
                import aiohttp
                
                async with aiohttp.ClientSession() as session:
                    async with asyncio.wait_for(
                        session.get(f"{self.cdp_url}/json/version"), 
                        timeout=self.connection_timeout
                    ) as response:
                        if response.status == 200:
                            version_info = await response.json()
                            logger.info(f"✅ Chrome detected: {version_info.get('Browser', 'Unknown version')}")
                            return True
                        return False
                        
            except ImportError:
                # aiohttp not available, skip availability check
                logger.debug("aiohttp not available, skipping Chrome availability check")
                return True  # Assume available for basic setups
        
        except (Exception,) as e:
            logger.debug(f"Chrome availability check failed: {e}")
            return False
    
    async def _setup_cdp_connection(self) -> Browser:
        """
        Connect to user's running Chrome via CDP with enhanced error handling.
        
        Returns:
            Browser instance connected to user's Chrome
            
        Raises:
            ConnectionError: If Chrome is not running with debug port (preserved for compatibility)
            ChromeConnectionTimeoutError: If connection times out
            CDPConnectionError: For other CDP-related issues
        """
        try:
            config = BrowserConfig(
                cdp_url=self.cdp_url,
                keep_alive=True,
                timeout=self.connection_timeout * 1000  # browser-use expects milliseconds
            )
            
            browser = Browser(config)
            
            # Initialize with timeout handling
            await asyncio.wait_for(browser._init(), timeout=self.connection_timeout)
            
            # Test connection health
            await self._verify_connection_health(browser)
            
            self._connection_healthy = True
            logger.info(f"🔗 Successfully connected to Chrome via CDP ({self.cdp_url})")
            
            return browser
            
        except asyncio.TimeoutError:
            raise ChromeConnectionTimeoutError(
                f"Timeout connecting to Chrome CDP after {self.connection_timeout}s"
            )
        except Exception as e:
            # Preserve ConnectionError for test compatibility
            if isinstance(e, ConnectionError):
                raise  # Re-raise original ConnectionError
            
            # Check if this is likely a Chrome not running scenario
            error_str = str(e).lower()
            if any(indicator in error_str for indicator in ['connection refused', 'not found', 'target closed']):
                raise ConnectionError(f"Chrome not found on port 9222")  # Use ConnectionError for compatibility
            else:
                raise CDPConnectionError(f"Failed to establish CDP connection: {str(e)}")
    
    async def _verify_connection_health(self, browser: Browser) -> bool:
        """
        Verify that the CDP connection is healthy and responsive.
        
        Args:
            browser: Browser instance to test
            
        Returns:
            True if connection is healthy
            
        Raises:
            CDPConnectionError: If connection is unhealthy
        """
        try:
            # Simple health check - try to get browser context
            if hasattr(browser, 'context') and browser.context:
                logger.debug("✅ CDP connection health check passed")
                return True
            else:
                raise CDPConnectionError("Browser context not available")
        except Exception as e:
            raise CDPConnectionError(f"CDP connection health check failed: {e}")
    
    async def _setup_fallback_browser(self) -> Browser:
        """
        Setup standalone browser as fallback when CDP connection fails.
        
        Returns:
            Browser instance using standalone mode
        """
        logger.info("🚀 Setting up standalone browser (fallback mode)")
        
        config = BrowserConfig(
            headless=False,
            keep_alive=False,
            user_data_dir=str(self.browser_data_dir)  # Use persistent data directory
        )
        
        browser = Browser(config)
        await browser._init()
        
        logger.info("✅ Standalone browser ready")
        return browser
    
    async def _get_browser_with_fallback(self) -> Browser:
        """
        Get browser instance with automatic fallback and retry logic.
        
        First tries CDP connection to user's Chrome, falls back to standalone browser.
        Includes retry logic for transient connection issues.
        
        Returns:
            Browser instance (CDP or fallback)
        """
        last_error = None
        
        # Try CDP connection with retries
        for attempt in range(self.max_retries):
            try:
                logger.info(f"🔄 Attempting CDP connection (attempt {attempt + 1}/{self.max_retries})")
                browser = await self._setup_cdp_connection()
                self._last_browser_instance = browser
                return browser
                
            except ChromeNotRunningError as e:
                # Don't retry if Chrome is not running - fail fast to fallback
                logger.warning(f"⚠️  Chrome not available: {e}")
                break
                
            except (ChromeConnectionTimeoutError, CDPConnectionError, ConnectionError) as e:
                last_error = e
                logger.warning(f"⚠️  CDP connection attempt {attempt + 1} failed: {e}")
                
                if attempt < self.max_retries - 1:
                    # Exponential backoff for retries
                    wait_time = 2 ** attempt
                    logger.info(f"⏳ Waiting {wait_time}s before retry...")
                    await asyncio.sleep(wait_time)
        
        # CDP connection failed - use fallback
        logger.info("🔄 CDP connection failed, switching to fallback browser...")
        self._connection_healthy = False
        
        try:
            browser = await self._setup_fallback_browser()
            self._last_browser_instance = browser
            return browser
        except Exception as fallback_error:
            # If both CDP and fallback fail, raise the most relevant error
            error_msg = f"Both CDP and fallback browser failed. CDP: {last_error}, Fallback: {fallback_error}"
            logger.error(f"❌ {error_msg}")
            raise CDPConnectionError(error_msg)
    
    def get_connection_status(self) -> dict:
        """
        Get current connection status information for UI display.
        
        Returns:
            Dictionary with connection status details
        """
        return {
            "cdp_url": self.cdp_url,
            "connection_healthy": self._connection_healthy,
            "has_browser_instance": self._last_browser_instance is not None,
            "browser_data_dir": str(self.browser_data_dir),
            "browser_data_exists": self.is_browser_data_present()
        }
    
    async def harvest(self, prompt: Optional[str]) -> Union[List[FetchedPost], str, List[Any]]:
        """
        Execute a natural language prompt on LinkedIn via browser-use Agent.
        
        Enhanced with CDP connection management and comprehensive error handling.
        
        Args:
            prompt: Natural language instruction for LinkedIn automation
            
        Returns:
            Agent execution results - can be string confirmation, 
            list of structured data, or parsed FetchedPost objects
            
        Raises:
            ValueError: If prompt is empty or None
            ConnectionError: For Chrome/browser connection issues (preserved for compatibility)
            CDPConnectionError: For CDP-specific issues
        """
        # Validate input
        if not prompt or not prompt.strip():
            raise ValueError("Empty prompt not allowed")
        
        # Clean the prompt
        clean_prompt = prompt.strip()
        
        # Enhanced prompt with LinkedIn-specific guidance and CDP awareness
        enhanced_prompt = f"""
        TASK: {clean_prompt}
        
        INSTRUCTIONS:
        1. Navigate to LinkedIn.com first
        2. If not logged in, PAUSE and ask user to login manually
        3. Once logged in, proceed with the task systematically
        4. Focus on LinkedIn content and interactions only
        5. Return structured data when possible
        6. Handle any connection issues gracefully
        
        CONTEXT: Using {'persistent Chrome session' if self._connection_healthy else 'standalone browser'}
        """
        
        try:
            # Get browser with CDP connection and fallback
            logger.info("🔧 Setting up browser connection...")
            browser = await self._get_browser_with_fallback()
            
            # Create browser-use Agent with configured browser
            logger.info("🤖 Initializing LinkedIn automation agent...")
            agent = Agent(
                task=enhanced_prompt,
                llm=self.llm,
                browser=browser
            )
            
            # Execute the task
            logger.info("🚀 Starting LinkedIn automation task...")
            result = await agent.run()
            
            logger.info("✅ LinkedIn automation task completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"❌ Harvest operation failed: {e}")
            # Preserve original exception types for test compatibility
            if isinstance(e, (ConnectionError, ValueError, CDPConnectionError)):
                raise  # Re-raise original exception
            else:
                # Only wrap truly unexpected exceptions
                raise ConnectionError(f"Unexpected error during harvest: {e}")
    
    def get_browser_data_path(self) -> str:
        """Get the path to the browser data directory."""
        return str(self.browser_data_dir)
    
    def clear_browser_data(self) -> None:
        """Clear saved browser data (logout from all sessions)."""
        import shutil
        if self.browser_data_dir.exists():
            shutil.rmtree(self.browser_data_dir)
            self.browser_data_dir.mkdir(parents=True, exist_ok=True)
            logger.info("✅ Browser data cleared. You'll need to log in again.")
    
    def is_browser_data_present(self) -> bool:
        """Check if browser data exists."""
        return self.browser_data_dir.exists() and any(self.browser_data_dir.iterdir())
    
    async def close(self):
        """Close browser connections and cleanup resources."""
        if self._last_browser_instance:
            try:
                # Cleanup browser instance if needed
                # browser-use handles its own cleanup, but we can reset our tracking
                self._last_browser_instance = None
                self._connection_healthy = False
                logger.info("🔄 Browser connections closed")
            except Exception as e:
                logger.warning(f"⚠️  Error during cleanup: {e}")
    
    def get_chrome_startup_command(self) -> str:
        """
        Get the Chrome startup command for users.
        
        Returns:
            Command string to start Chrome with remote debugging
        """
        return f"chrome --remote-debugging-port=9222 --user-data-dir={self.browser_data_dir}"
