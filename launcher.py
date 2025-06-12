"""
Ultra-Lean LinkedIn AI Agent Launcher

Single orchestrator that coordinates:
- Chrome startup with CDP debugging
- Flask web application startup  
- APScheduler initialization
- Browser opening to localhost:5000
- Graceful shutdown handling

Usage:
    python launcher.py

This is the keystone component for the ultra-lean developer-focused architecture.
"""

import os
import signal
import subprocess
import threading
import time
import webbrowser
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler

# Import Flask app from our existing application
from app import app


class Launcher:
    """Main orchestrator for LinkedIn AI Agent ultra-lean architecture"""
    
    def __init__(self, chrome_debug_port: int = 9222, flask_port: int = 5000, 
                 flask_host: str = 'localhost', user_data_dir: Optional[str] = None):
        """Initialize Launcher with configuration parameters"""
        self.chrome_debug_port = chrome_debug_port
        self.flask_port = flask_port
        self.flask_host = flask_host
        self.user_data_dir = user_data_dir or os.path.expanduser('~/.linkedin_browser')
        
        # Component tracking
        self.chrome_process: Optional[subprocess.Popen] = None
        self.flask_thread: Optional[threading.Thread] = None
        self.scheduler: Optional[BackgroundScheduler] = None
        self.running: bool = False
    
    def start_chrome(self) -> None:
        """Start Chrome with CDP debugging enabled and persistent user data"""
        chrome_args = [
            self._get_chrome_executable(),
            f'--remote-debugging-port={self.chrome_debug_port}',
            f'--user-data-dir={self.user_data_dir}',
            '--no-first-run',
            '--disable-default-apps',
            '--disable-extensions-except',
            '--disable-component-extensions-with-background-pages'
        ]
        
        self.chrome_process = subprocess.Popen(chrome_args)
        print(f"✅ Chrome started with CDP debugging on port {self.chrome_debug_port}")
    
    def start_flask(self) -> None:
        """Start Flask web server in a separate thread"""
        def run_flask():
            app.run(
                host=self.flask_host,
                port=self.flask_port,
                debug=False
            )
        
        self.flask_thread = threading.Thread(target=run_flask, daemon=True)
        self.flask_thread.start()
        print(f"✅ Flask web UI started at http://{self.flask_host}:{self.flask_port}")
    
    def start_scheduler(self) -> None:
        """Initialize and start APScheduler for background jobs"""
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        print("✅ APScheduler started for background job execution")
    
    def open_browser(self) -> None:
        """Open browser to the Flask web UI"""
        url = f'http://{self.flask_host}:{self.flask_port}'
        webbrowser.open(url)
        print(f"✅ Browser opened to {url}")
    
    def start(self) -> None:
        """Start all components in the correct order"""
        print("🚀 Starting LinkedIn AI Agent Ultra-Lean Platform...")
        
        self.start_chrome()
        time.sleep(2)  # Give Chrome time to start CDP
        
        self.start_flask()
        time.sleep(1)  # Give Flask time to start
        
        self.start_scheduler()
        
        self.open_browser()
        
        self.running = True
        print("✅ All components started successfully!")
        print("📝 Use the web interface to create and schedule LinkedIn automation")
    
    def stop(self) -> None:
        """Gracefully shutdown all components"""
        print("🛑 Shutting down LinkedIn AI Agent...")
        
        # Stop scheduler
        if hasattr(self, 'scheduler') and self.scheduler and self.scheduler.running:
            self.scheduler.shutdown()
            print("✅ Scheduler stopped")
        
        # Stop Flask (it's in a daemon thread, so it will stop automatically)
        if hasattr(self, 'flask_thread') and self.flask_thread.is_alive():
            print("✅ Flask server stopped")
        
        # Stop Chrome
        if hasattr(self, 'chrome_process') and self.chrome_process:
            try:
                self.chrome_process.terminate()
                self.chrome_process.wait(timeout=5)
                print("✅ Chrome stopped")
            except subprocess.TimeoutExpired:
                self.chrome_process.kill()
                print("✅ Chrome force-stopped")
        
        self.running = False
        print("✅ Shutdown complete")
    
    def setup_signal_handlers(self) -> None:
        """Register signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            print(f"\n📡 Received signal {signum}, initiating graceful shutdown...")
            self.stop()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def _get_chrome_executable(self) -> str:
        """Get the Chrome executable path for the current platform"""
        import platform
        system = platform.system()
        
        if system == "Darwin":  # macOS
            return "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        elif system == "Windows":
            # Common Chrome installation paths on Windows
            possible_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    return path
            return "chrome"  # Fallback to PATH
        else:  # Linux and other Unix-like systems
            return "google-chrome"


def main():
    """Main entry point for the LinkedIn AI Agent launcher"""
    print("🎯 LinkedIn AI Agent - Ultra-Lean Developer Platform")
    print("=" * 55)
    
    # Create and configure launcher
    launcher = Launcher()
    launcher.setup_signal_handlers()
    
    try:
        # Start all components
        launcher.start()
        
        # Keep the program running
        while launcher.running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n⌨️  Keyboard interrupt received")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        launcher.stop()


if __name__ == "__main__":
    main()
