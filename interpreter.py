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

    def __init__(self, api_key: str):
        """Initialize the PromptInterpreter and load the OpenAI API key from the environment."""
        if not api_key:
            raise ValueError("OpenAI API key was not provided to PromptInterpreter.")
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
        "topic": "string",          // The main subject or keyword for the LinkedIn search.
        "post_limit": "integer",      // The number of posts to engage with or fetch.
        "engagement_type": "array of strings ('like', 'comment', 'share', 'fetch_posts')", // The type of action to perform. 'fetch_posts' means to retrieve post details.
        "is_valid": "boolean",        // True if the prompt is clear and actionable, false otherwise.
        "feedback": "string"         // Constructive feedback if is_valid is false, explaining what's missing or ambiguous. Empty if is_valid is true.
    }

    **Key Rules:**
    - If the prompt clearly specifies a topic, post limit, and a valid engagement_type (like, comment, share, fetch_posts), set `is_valid` to `true` and `feedback` to `""`.
    - If the prompt is missing any of these key details (topic, post_limit for engagement types other than fetch_posts where it can be defaulted, engagement_type), or if the engagement_type is not one of the allowed values, set `is_valid` to `false`.
    - For invalid prompts, attempt to fill in any information you can discern (like the topic or partial engagement type). Set missing numbers to `0`. Provide helpful `feedback` explaining what's missing or why it's invalid.
    - For 'fetch_posts' engagement_type: if `post_limit` is not specified, default it to `5` and set `is_valid` to `true` if a topic is present.
    - For other engagement_types ('like', 'comment', 'share'): if `post_limit` is missing or 0, set `is_valid` to `false` and provide feedback.

    **Example 1: Valid 'comment' Prompt**
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

    **Example 2: Valid 'like' and 'share' Prompt**
    - User Prompt: "Like 3 posts on python programming and also share them."
    - JSON Output:
    ```json
    {
        "topic": "python programming",
        "post_limit": 3,
        "engagement_type": ["like", "share"],
        "is_valid": true,
        "feedback": ""
    }
    ```

    **Example 3: Valid 'fetch_posts' Prompt (explicit limit)**
    - User Prompt: "Fetch 10 posts about AI in healthcare."
    - JSON Output:
    ```json
    {
        "topic": "AI in healthcare",
        "post_limit": 10,
        "engagement_type": ["fetch_posts"],
        "is_valid": true,
        "feedback": ""
    }
    ```

    **Example 4: Valid 'fetch_posts' Prompt (implicit limit)**
    - User Prompt: "Get me articles on renewable energy."
    - JSON Output:
    ```json
    {
        "topic": "renewable energy",
        "post_limit": 5, 
        "engagement_type": ["fetch_posts"],
        "is_valid": true,
        "feedback": ""
    }
    ```

    **Example 5: Invalid Prompt (missing engagement type)**
    - User Prompt: "Show me 2 things about marketing."
    - JSON Output:
    ```json
    {
        "topic": "marketing",
        "post_limit": 2,
        "engagement_type": [],
        "is_valid": false,
        "feedback": "Please specify a valid engagement type (e.g., like, comment, share, fetch_posts)."
    }
    ```

    **Example 6: Invalid Prompt (missing topic for 'like')**
    - User Prompt: "Like 5 posts."
    - JSON Output:
    ```json
    {
        "topic": "",
        "post_limit": 5,
        "engagement_type": ["like"],
        "is_valid": false,
        "feedback": "Please specify a topic for the posts."
    }
    ```

    **Example 7: Invalid Prompt (missing post_limit for 'comment')**
    - User Prompt: "Comment on posts about fintech."
    - JSON Output:
    ```json
    {
        "topic": "fintech",
        "post_limit": 0,
        "engagement_type": ["comment"],
        "is_valid": false,
        "feedback": "Please specify how many posts you'd like to comment on."
    }
    ```

    **Example 8: Valid 'fetch_posts' Prompt (alternative phrasing, explicit limit)**
    - User Prompt: "Find 2 articles about space exploration."
    - JSON Output:
    ```json
    {
        "topic": "space exploration",
        "post_limit": 2,
        "engagement_type": ["fetch_posts"],
        "is_valid": true,
        "feedback": ""
    }
    ```

    Remember, your ONLY output should be the JSON object based on these rules and examples.
    """
