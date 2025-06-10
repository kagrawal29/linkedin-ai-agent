# tests/test_harvester.py

import pytest
from unittest.mock import patch, MagicMock, AsyncMock

# This import will fail as harvester.py is not yet implemented.
from harvester import Harvester
from interpreter import Command

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
    mock_agent_class.assert_called_once()
    called_args, called_kwargs = mock_agent_class.call_args
    assert called_kwargs.get('task') == expected_task
    
    # Verify the agent's `run` method was called.
    mock_agent_instance.run.assert_awaited_once()

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

    mock_agent_class.assert_called_once()
    called_args, called_kwargs = mock_agent_class.call_args
    assert called_kwargs.get('task') == expected_task
    
    mock_agent_instance.run.assert_awaited_once()
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

    mock_agent_class.assert_called_once()
    called_args, called_kwargs = mock_agent_class.call_args
    assert called_kwargs.get('task') == expected_task
    
    mock_agent_instance.run.assert_awaited_once()
    assert result == "Connection requests sent."
