"""
Test suite for launcher.py - Single orchestrator for ultra-lean LinkedIn AI Agent

Tests for the main launcher module that coordinates:
- Chrome startup with CDP debugging
- Flask web application startup
- APScheduler initialization
- Browser opening to localhost:5000
- Graceful shutdown handling

Following TDD methodology: RED-GREEN-REFACTOR
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import threading
import time
import subprocess
import sys
import os

# Import the launcher module (will be created)
try:
    from launcher import Launcher, main
except ImportError:
    # Expected during RED phase - launcher.py doesn't exist yet
    pass


class TestLauncher:
    """Test suite for Launcher class"""
    
    def test_launcher_init_sets_default_configuration(self):
        """Test that Launcher initializes with default configuration"""
        launcher = Launcher()
        
        assert launcher.chrome_debug_port == 9222
        assert launcher.flask_port == 5000
        assert launcher.flask_host == 'localhost'
        assert launcher.user_data_dir == os.path.expanduser('~/.linkedin_browser')
        assert launcher.chrome_process is None
        assert launcher.flask_thread is None
        assert launcher.scheduler is None
        assert launcher.running is False
    
    def test_launcher_init_accepts_custom_configuration(self):
        """Test that Launcher accepts custom configuration parameters"""
        launcher = Launcher(
            chrome_debug_port=9223,
            flask_port=5001,
            flask_host='127.0.0.1',
            user_data_dir='/custom/path'
        )
        
        assert launcher.chrome_debug_port == 9223
        assert launcher.flask_port == 5001
        assert launcher.flask_host == '127.0.0.1'
        assert launcher.user_data_dir == '/custom/path'
    
    @patch('launcher.subprocess.Popen')
    def test_start_chrome_launches_with_correct_flags(self, mock_popen):
        """Test that Chrome is started with correct CDP and user data flags"""
        mock_process = Mock()
        mock_popen.return_value = mock_process
        
        launcher = Launcher()
        launcher.start_chrome()
        
        # Verify Chrome was started with correct arguments
        mock_popen.assert_called_once()
        args = mock_popen.call_args[0][0]
        
        assert '--remote-debugging-port=9222' in args
        assert '--user-data-dir=' + launcher.user_data_dir in args
        assert '--no-first-run' in args
        assert '--disable-default-apps' in args
        assert launcher.chrome_process == mock_process
    
    @patch('launcher.app.run')
    def test_start_flask_launches_web_server(self, mock_flask_run):
        """Test that Flask web server is started in a separate thread"""
        launcher = Launcher()
        launcher.start_flask()
        
        # Wait a moment for thread to start and complete (since it's mocked)
        time.sleep(0.2)
        
        # Verify Flask was started with correct parameters
        mock_flask_run.assert_called_once_with(
            host=launcher.flask_host,
            port=launcher.flask_port,
            debug=False
        )
        
        # Verify thread was created
        assert launcher.flask_thread is not None
        # Note: Thread may have finished since app.run() was mocked and returned immediately
    
    @patch('launcher.BackgroundScheduler')
    def test_start_scheduler_initializes_apscheduler(self, mock_scheduler_class):
        """Test that APScheduler is initialized and started"""
        mock_scheduler = Mock()
        mock_scheduler_class.return_value = mock_scheduler
        
        launcher = Launcher()
        launcher.start_scheduler()
        
        # Verify scheduler was created and started
        mock_scheduler_class.assert_called_once()
        mock_scheduler.start.assert_called_once()
        assert launcher.scheduler == mock_scheduler
    
    @patch('launcher.webbrowser.open')
    def test_open_browser_opens_localhost_url(self, mock_browser_open):
        """Test that browser opens to correct localhost URL"""
        launcher = Launcher()
        launcher.open_browser()
        
        expected_url = f'http://{launcher.flask_host}:{launcher.flask_port}'
        mock_browser_open.assert_called_once_with(expected_url)
    
    @patch('launcher.Launcher.start_chrome')
    @patch('launcher.Launcher.start_flask')
    @patch('launcher.Launcher.start_scheduler')
    @patch('launcher.Launcher.open_browser')
    @patch('launcher.time.sleep')
    def test_start_launches_all_components(self, mock_sleep, mock_open_browser, mock_start_scheduler, 
                                         mock_start_flask, mock_start_chrome):
        """Test that start() method launches all components in correct order"""
        launcher = Launcher()
        launcher.start()
        
        # Verify all components were started
        mock_start_chrome.assert_called_once()
        mock_start_flask.assert_called_once()
        mock_start_scheduler.assert_called_once()
        mock_open_browser.assert_called_once()
        
        # Verify time.sleep was called (for startup delays)
        assert mock_sleep.call_count == 2  # Should be called twice: sleep(2) and sleep(1)
        
        # Verify running flag is set
        assert launcher.running is True
    
    def test_stop_gracefully_shuts_down_all_components(self):
        """Test that stop() method gracefully shuts down all components"""
        launcher = Launcher()
        
        # Mock running components
        mock_chrome = Mock()
        mock_flask_thread = Mock()
        mock_scheduler = Mock()
        
        launcher.chrome_process = mock_chrome
        launcher.flask_thread = mock_flask_thread
        launcher.scheduler = mock_scheduler
        launcher.running = True
        
        launcher.stop()
        
        # Verify all components were stopped
        mock_chrome.terminate.assert_called_once()
        mock_flask_thread.join.assert_called_once_with(timeout=5)
        mock_scheduler.shutdown.assert_called_once()
        
        # Verify running flag is cleared
        assert launcher.running is False
    
    @patch('launcher.signal.signal')
    def test_setup_signal_handlers_registers_shutdown_handlers(self, mock_signal):
        """Test that signal handlers are registered for graceful shutdown"""
        launcher = Launcher()
        launcher.setup_signal_handlers()
        
        # Verify signal handlers were registered
        assert mock_signal.call_count == 2
        # Check that SIGINT and SIGTERM handlers were registered
        calls = mock_signal.call_args_list
        signals_registered = [call[0][0] for call in calls]
        
        import signal
        assert signal.SIGINT in signals_registered
        assert signal.SIGTERM in signals_registered


class TestMainFunction:
    """Test suite for main() function"""
    
    @patch('launcher.Launcher')
    @patch('launcher.time.sleep')
    def test_main_creates_launcher_and_starts(self, mock_sleep, mock_launcher_class):
        """Test that main() creates Launcher instance and starts it"""
        mock_launcher = Mock()
        # Set running to False immediately to prevent infinite loop
        mock_launcher.running = False
        mock_launcher_class.return_value = mock_launcher
        
        main()
        
        # Verify Launcher was created and started
        mock_launcher_class.assert_called_once()
        mock_launcher.setup_signal_handlers.assert_called_once()
        mock_launcher.start.assert_called_once()
        # Since running is immediately False, sleep shouldn't be called
        mock_sleep.assert_not_called()
    
    @patch('launcher.Launcher')
    @patch('launcher.time.sleep')
    def test_main_keeps_running_until_interrupted(self, mock_sleep, mock_launcher_class):
        """Test that main() keeps the program running until interrupted"""
        mock_launcher = Mock()
        # Set up the running attribute to become False after first sleep call
        mock_launcher.running = True
        mock_launcher_class.return_value = mock_launcher
        
        # Create a counter to make running False after first iteration
        call_count = [0]
        def sleep_side_effect(*args):
            call_count[0] += 1
            if call_count[0] == 1:
                mock_launcher.running = False
            
        mock_sleep.side_effect = sleep_side_effect
        
        main()
        
        # Verify the components were properly called
        mock_launcher_class.assert_called_once()
        mock_launcher.setup_signal_handlers.assert_called_once()
        mock_launcher.start.assert_called_once()
        mock_sleep.assert_called()
        mock_launcher.stop.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__])
