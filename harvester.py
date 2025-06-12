# harvester.py

import asyncio
import os
from pathlib import Path
from browser_use import Agent
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from models import FetchedPost
from typing import Union, List, Optional, Any

load_dotenv()

"""
Harvester module for executing LinkedIn tasks via browser automation.

This module has been simplified to accept natural language prompts directly
and pass them to browser-use Agent, eliminating the need for command parsing.
"""

class Harvester:
    """
    Simplified harvester that executes natural language prompts on LinkedIn.
    
    Replaces the complex command-based approach with direct prompt passing
    to browser-use Agent for maximum flexibility.
    """
    
    def __init__(self):
        """Initialize the Harvester with an LLM."""
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        
        # Set up browser data directory for future persistence
        self.browser_data_dir = Path.home() / ".linkedin_ai_agent" / "browser_data"
        self.browser_data_dir.mkdir(parents=True, exist_ok=True)
    
    async def harvest(self, prompt: Optional[str]) -> Union[List[FetchedPost], str, List[Any]]:
        """
        Execute a natural language prompt on LinkedIn via browser-use Agent.
        
        Args:
            prompt: Natural language instruction for LinkedIn automation
            
        Returns:
            Agent execution results - can be string confirmation, 
            list of structured data, or parsed FetchedPost objects
            
        Raises:
            ValueError: If prompt is empty or None
        """
        # Validate input
        if not prompt or not prompt.strip():
            raise ValueError("Empty prompt not allowed")
        
        # Clean the prompt
        clean_prompt = prompt.strip()
        
        # Enhanced prompt with LinkedIn-specific guidance
        enhanced_prompt = f"""
        TASK: {clean_prompt}
        
        INSTRUCTIONS:
        1. Navigate to LinkedIn.com first
        2. If not logged in, PAUSE and wait for manual login
        3. Once logged in, proceed with the task
        4. Focus on LinkedIn content and interactions only
        5. Return structured data when possible
        """
        
        # Create browser-use Agent with basic configuration
        agent = Agent(
            task=enhanced_prompt,
            llm=self.llm
        )
        
        result = await agent.run()
        
        return result
    
    def get_browser_data_path(self) -> str:
        """Get the path to the browser data directory."""
        return str(self.browser_data_dir)
    
    def clear_browser_data(self) -> None:
        """Clear saved browser data (logout from all sessions)."""
        import shutil
        if self.browser_data_dir.exists():
            shutil.rmtree(self.browser_data_dir)
            self.browser_data_dir.mkdir(parents=True, exist_ok=True)
            print("✅ Browser data cleared. You'll need to log in again.")
    
    def is_browser_data_present(self) -> bool:
        """Check if browser data exists."""
        return self.browser_data_dir.exists() and any(self.browser_data_dir.iterdir())
    
    async def close(self):
        """Close method for compatibility."""
        pass  # Agent handles its own cleanup
