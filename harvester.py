# harvester.py

import asyncio
from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv

from interpreter import Command
from models import FetchedPost # Added
from typing import List, Union # Added

load_dotenv()

class Harvester:
    """
    Uses the browser-use agent to perform actions on LinkedIn based on a command.
    """

    def __init__(self):
        """Initializes the Harvester with an LLM."""
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)

    async def harvest(self, command: Command) -> Union[List[FetchedPost], str]: # Return type changed
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
        elif engagement == "fetch_posts":
            task = (
                f"Go to linkedin.com, log in if needed. Search for posts about '{command.topic}'. "
                f"Extract details (post_id, post_url, author_name, author_url, author_headline, content_text, "
                f"posted_timestamp_str, likes_count, comments_count, reposts_count, views_count) "
                f"for the first {command.post_limit} relevant posts. Return this information as a list of structured objects."
            )
        else:
            # Fallback for any other unimplemented engagement types
            task = f"Go to linkedin.com, log in if needed, and then {engagement} {command.post_limit} posts about '{command.topic}'."

        print(f"Executing Harvester task: {task}")

        agent = Agent(
            llm=self.llm, # task removed from constructor
        )
        agent_output = await agent.run(task=task) # task passed to run method

        if engagement == "fetch_posts":
            if isinstance(agent_output, list):
                fetched_posts = []
                for item_data in agent_output:
                    if isinstance(item_data, dict):
                        try:
                            fetched_posts.append(FetchedPost(**item_data))
                        except Exception as e: # Catch Pydantic validation errors or other issues
                            print(f"Error parsing item into FetchedPost: {item_data}, Error: {e}")
                            # Decide if we want to skip this item or handle error differently
                    else:
                        print(f"Warning: Expected a dict from agent output for post item, got {type(item_data)}")
                return fetched_posts
            else:
                print(f"Warning: Expected a list from agent for 'fetch_posts', got {type(agent_output)}")
                return [] # Return empty list if agent output is not a list
        else:
            # For other engagement types, they currently expect a string result.
            # For type consistency with List[FetchedPost], we return an empty list for now.
            # This will need to be refactored if these engagements should also return posts
            # or if the harvest method should have a more generic return type (e.g., Union[str, List[FetchedPost]]).
            print(f"Agent output for '{engagement}': {agent_output}") # Keep this to see what agent returns
            return str(agent_output) # Return the agent's output as a string
