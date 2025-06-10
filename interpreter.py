# interpreter.py

from pydantic import BaseModel
from typing import List
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

class Command(BaseModel):
    """A structured command parsed from a user's natural language prompt."""
    topic: str
    post_limit: int
    engagement_type: List[str]
    is_valid: bool
    feedback: str

class PromptInterpreter:
    """The 'translator' that converts natural language prompts into Commands."""

    def __init__(self):
        """Initialize the PromptInterpreter and load the OpenAI API key from the environment."""
        # Build a reliable path to the .env file in the project root
        project_root = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.join(project_root, '.env')
        
        load_dotenv(dotenv_path=dotenv_path)
        api_key = os.getenv("OpenAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI_API_KEY not found. Please ensure it is set in the .env file at the project root.")
        self.client = OpenAI(api_key=api_key)
        self.system_prompt = self._build_system_prompt()

    def parse_prompt(self, prompt: str) -> Command:
        """
        Parse the user's natural language prompt into a structured Command object
        using the OpenAI API with GPT-4.1.
        
        Args:
            prompt: The user's natural language prompt
            
        Returns:
            A Command object with structured information extracted from the prompt
        """
        try:
            completion = self.client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                response_format=Command
            )

            message = completion.choices[0].message
            if message.parsed:
                return message.parsed
            else:
                return Command(
                    topic="",
                    post_limit=0,
                    engagement_type=[],
                    is_valid=False,
                    feedback=f"The model refused to provide a valid command: {message.refusal}"
                )

        except Exception as e:
            return Command(
                topic="",
                post_limit=0,
                engagement_type=[],
                is_valid=False,
                feedback=f"An unexpected error occurred: {e}"
            )

    def _build_system_prompt(self) -> str:
        """
        Builds the system prompt that instructs the LLM on how to parse the user's request.
        
        Returns:
            A string containing the system prompt for the LLM
        """
        return """
    You are an expert command parser for a LinkedIn engagement bot. Your task is to analyze a user's prompt and create a structured JSON object. Your ONLY output must be the JSON object.

    The JSON object must have this schema:
    {
        "topic": "string",
        "post_limit": "integer",
        "engagement_type": "array of strings ('like', 'comment', 'share')",
        "is_valid": "boolean",
        "feedback": "string"
    }

    **Key Rules:**
    - If the prompt clearly specifies a topic, post limit, and engagement type, set `is_valid` to `true` and `feedback` to `""`.
    - If the prompt is missing any of these key details, set `is_valid` to `false`.
    - For invalid prompts, fill in any information you can find (like the topic), set missing numbers to `0` and missing lists to `[]`, and provide a helpful `feedback` message explaining what's missing.

    **Example 1: Valid Prompt**
    - User Prompt: "Could you comment on 5 recent posts about systems thinking?"
    - JSON Output:
    ```json
    {
        "topic": "systems thinking",
        "post_limit": 5,
        "engagement_type": ["comment"],
        "is_valid": true,
        "feedback": ""
    }
    ```

    **Example 2: Invalid Prompt (Missing Limit & Type)**
    - User Prompt: "Engage with some posts about AI."
    - JSON Output:
    ```json
    {
        "topic": "AI",
        "post_limit": 0,
        "engagement_type": [],
        "is_valid": false,
        "feedback": "The prompt is too ambiguous. Please specify the number of posts and the engagement type (e.g., 'like', 'comment')."
    }
    ```

    **Example 3: Invalid Prompt (Missing Topic)**
    - User Prompt: "Like 10 posts for me."
    - JSON Output:
    ```json
    {
        "topic": "",
        "post_limit": 10,
        "engagement_type": ["like"],
        "is_valid": false,
        "feedback": "The prompt is too ambiguous. Please specify a topic for the posts."
    }
    ```
    """
