# harvester.py

import asyncio
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
        """Initialize the Harvester with an LLM for the browser-use Agent."""
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
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
        
        # Create and execute browser-use Agent with the prompt
        agent = Agent(llm=self.llm, task=clean_prompt)
        result = await agent.run()
        
        # Return the agent's result directly
        # The agent can return various types (string, list, etc.)
        return result
