# tests/test_harvester.py
from typing import List # Added for type hinting

import pytest
from unittest.mock import patch, MagicMock, AsyncMock

# This import will fail as harvester.py is not yet implemented.
from harvester import Harvester
from interpreter import Command
from models import FetchedPost # Added import

@pytest.mark.asyncio
@patch('harvester.Agent', new_callable=MagicMock)
async def test_harvester_executes_like_command(mock_agent_class):
    """
    RED: Tests that the Harvester correctly translates a 'like' command
    into a natural language task and executes it with the browser-use Agent.
    """
    # Arrange
    # Mock the agent's async `run` method to avoid actual browser interaction.
    mock_agent_instance = MagicMock()
    mock_agent_instance.run = AsyncMock(return_value="Task completed successfully.")
    mock_agent_class.return_value = mock_agent_instance

    harvester = Harvester()
    command = Command(
            topic="AI in healthcare",
            post_limit=5,
            engagement_type=["like"],
            is_valid=True,
            feedback="Command is valid and ready for harvesting."
        )

    # Act
    # The harvest method will be async in the new implementation.
    result = await harvester.harvest(command)

    # Assert
    expected_task = "Go to linkedin.com, log in if needed, and then like 5 posts about 'AI in healthcare'."

    # Verify that the Agent class was instantiated correctly.
    mock_agent_class.assert_called_once() # Agent is instantiated
    # called_args, called_kwargs = mock_agent_class.call_args # No longer checking constructor args for task
    
    # Verify the agent's `run` method was called with the correct task keyword argument.
    mock_agent_instance.run.assert_awaited_once_with(task=expected_task)

    # Verify the result from the agent is returned.
    assert result == "Task completed successfully."


@pytest.mark.asyncio
@patch('harvester.Agent', new_callable=MagicMock)
async def test_harvester_executes_comment_command(mock_agent_class):
    """
    RED: Tests that the Harvester correctly translates a 'comment' command
    into a natural language task and executes it with the browser-use Agent.
    """
    # Arrange
    mock_agent_instance = MagicMock()
    mock_agent_instance.run = AsyncMock(return_value="Comments drafted successfully.")
    mock_agent_class.return_value = mock_agent_instance

    harvester = Harvester()
    command = Command(
            topic="sustainable energy solutions",
            post_limit=3,
            engagement_type=["comment"],
            is_valid=True,
            feedback="Command is valid and ready for harvesting."
        )

    # Act
    result = await harvester.harvest(command)

    # Assert
    expected_task = "Go to linkedin.com, log in if needed, find 3 posts about 'sustainable energy solutions', and then draft a relevant comment for each."

    mock_agent_class.assert_called_once() # Agent is instantiated
    # called_args, called_kwargs = mock_agent_class.call_args # No longer checking constructor args for task
    
    # Verify the agent's `run` method was called with the correct task keyword argument.
    mock_agent_instance.run.assert_awaited_once_with(task=expected_task)
    assert result == "Comments drafted successfully."


@pytest.mark.asyncio
@patch('harvester.Agent', new_callable=MagicMock)
async def test_harvester_executes_connect_command(mock_agent_class):
    """
    RED: Tests that the Harvester correctly translates a 'connect' command
    into a natural language task and executes it with the browser-use Agent.
    """
    # Arrange
    mock_agent_instance = MagicMock()
    mock_agent_instance.run = AsyncMock(return_value="Connection requests sent.")
    mock_agent_class.return_value = mock_agent_instance

    harvester = Harvester()
    command = Command(
            topic="Product Managers in tech",  # Topic might represent the role/industry to connect with
            post_limit=2,  # Using post_limit to mean number of connections for now
            engagement_type=["connect"],
            is_valid=True,
            feedback="Command is valid and ready for harvesting."
        )

    # Act
    result = await harvester.harvest(command)

    # Assert
    # For 'connect', the task is more about finding people than posts.
    # The 'topic' could be interpreted as criteria for people search.
    # The 'post_limit' could be interpreted as the number of connection requests.
    expected_task = "Go to linkedin.com, log in if needed, find 2 people who are 'Product Managers in tech', and then send connection requests."

    mock_agent_class.assert_called_once() # Agent is instantiated
    # called_args, called_kwargs = mock_agent_class.call_args # No longer checking constructor args for task
    
    # Verify the agent's `run` method was called with the correct task keyword argument.
    mock_agent_instance.run.assert_awaited_once_with(task=expected_task)
    assert result == "Connection requests sent."


@pytest.mark.asyncio
@patch('harvester.Agent', new_callable=MagicMock) # Patching Agent in harvester module
async def test_harvester_fetches_posts_and_returns_structured_data(mock_agent_class):
    """
    RED: Tests that the Harvester correctly fetches posts based on a command,
    parses the agent's output, and returns a list of FetchedPost objects.
    """
    # Arrange
    mock_agent_instance = MagicMock()
    # Simulate the agent returning structured data (e.g., a list of dicts)
    # This data should be parsable into FetchedPost objects.
    sample_agent_output = [
        {
            "post_id": "urn:li:activity:1",
            "post_url": "https://www.linkedin.com/feed/update/urn:li:activity:1/",
            "author_name": "Author One",
            "author_url": "https://www.linkedin.com/in/authorone/",
            "author_headline": "Headline One",
            "content_text": "Content of post one.",
            "posted_timestamp_str": "1h",
            "likes_count": 10,
            "comments_count": 2,
            "reposts_count": 1,
            "views_count": 100
        },
        {
            "post_id": "urn:li:activity:2",
            "post_url": "https://www.linkedin.com/feed/update/urn:li:activity:2/",
            "author_name": "Author Two",
            "author_url": "https://www.linkedin.com/in/authortwo/",
            "author_headline": "Headline Two",
            "content_text": "Content of post two.",
            "posted_timestamp_str": "2d",
            "likes_count": 20,
            "comments_count": 5,
            "reposts_count": 3,
            "views_count": 200
        }
    ]
    mock_agent_instance.run = AsyncMock(return_value=sample_agent_output)
    mock_agent_class.return_value = mock_agent_instance

    harvester = Harvester()
    command = Command(
        topic="AI in fintech",
        post_limit=2,
        engagement_type=["fetch_posts"], # Specific engagement type for fetching
        is_valid=True,
        feedback="Command is valid for fetching posts."
    )

    # Act
    result: List[FetchedPost] = await harvester.harvest(command)

    # Assert
    # 1. Task string generation for the agent (new or modified logic in Harvester)
    expected_task_for_agent = (
        f"Go to linkedin.com, log in if needed. Search for posts about '{command.topic}'. "
        f"Extract details (post_id, post_url, author_name, author_url, author_headline, content_text, "
        f"posted_timestamp_str, likes_count, comments_count, reposts_count, views_count) "
        f"for the first {command.post_limit} relevant posts. Return this information as a list of structured objects."
    )
    
    mock_agent_class.assert_called_once() # Agent should be instantiated
    called_args, called_kwargs = mock_agent_class.call_args
    # We expect the Harvester to now pass the task to the agent instance's run method, not at instantiation
    # So, we check the call to agent_instance.run()
    mock_agent_instance.run.assert_awaited_once_with(task=expected_task_for_agent) # Assert with task as keyword argument

    # 2. Result type and content
    assert isinstance(result, list), "Result should be a list."
    assert len(result) == len(sample_agent_output), "Result list length should match sample output."
    
    for i, post in enumerate(result):
        assert isinstance(post, FetchedPost), f"Item {i} in result should be a FetchedPost object."
        # Compare some key fields to ensure data is correctly parsed
        assert post.post_id == sample_agent_output[i]["post_id"]
        assert str(post.post_url) == sample_agent_output[i]["post_url"] # Pydantic HttpUrl to str for comparison
        assert post.author_name == sample_agent_output[i]["author_name"]
        assert post.content_text == sample_agent_output[i]["content_text"]
        assert post.likes_count == sample_agent_output[i]["likes_count"]
