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
        engagement = command.engagement_type[0]
        if engagement == "like":
            task = f"Go to linkedin.com, log in if needed, and then like {command.post_limit} posts about '{command.topic}'."
        elif engagement == "comment":
            task = f"Go to linkedin.com, log in if needed, find {command.post_limit} posts about '{command.topic}', and then draft a relevant comment for each."
        elif engagement == "connect":
            # For 'connect', topic describes the person, post_limit is number of connections
            task = f"Go to linkedin.com, log in if needed, find {command.post_limit} people who are '{command.topic}', and then send connection requests."
        else:
            # Fallback for any other unimplemented engagement types
            task = f"Go to linkedin.com, log in if needed, and then {engagement} {command.post_limit} posts about '{command.topic}'."

        print(f"Executing Harvester task: {task}")

        agent = Agent(
            task=task,
            llm=self.llm,
        )
        result = await agent.run()
        return result
