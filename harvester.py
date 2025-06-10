# harvester.py

import asyncio
from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv

from interpreter import Command

load_dotenv()

class Harvester:
    """
    Uses the browser-use agent to perform actions on LinkedIn based on a command.
    """

    def __init__(self):
        """Initializes the Harvester with an LLM."""
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)

    async def harvest(self, command: Command) -> str:
        """
        Translates a Command object into a natural language task and executes it.
        """
        task = f"Go to linkedin.com, log in if needed, and then {command.engagement_type[0]} {command.post_limit} posts about '{command.topic}'."

        print(f"Executing Harvester task: {task}")

        agent = Agent(
            task=task,
            llm=self.llm,
        )
        result = await agent.run()
        return result
