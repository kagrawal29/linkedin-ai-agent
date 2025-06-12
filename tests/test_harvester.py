from typing import List, Union

import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from harvester import Harvester
from models import FetchedPost


@pytest.mark.asyncio
@patch('harvester.Agent', new_callable=MagicMock)
async def test_harvester_executes_natural_language_prompt(mock_agent_class):
    """
    RED: Tests that the Harvester correctly passes natural language prompts
    directly to the browser-use Agent without command parsing.
    """
    # Arrange
    mock_agent_instance = MagicMock()
    mock_agent_instance.run = AsyncMock(return_value="Task completed successfully.")
    mock_agent_class.return_value = mock_agent_instance

    harvester = Harvester()
    prompt = "Go to LinkedIn and like 5 posts about AI in healthcare"

    # Act
    result = await harvester.harvest(prompt)

    # Assert
    # Verify that the Agent class was instantiated correctly
    mock_agent_class.assert_called_once()
    call_args = mock_agent_class.call_args
    assert call_args[1]['llm'] is not None  # LLM should be passed
    assert call_args[1]['browser_config'] is not None  # Browser config should be passed
    assert 'user_data_dir' in call_args[1]['browser_config']  # Should have persistent data dir
    assert prompt in call_args[1]['task']  # Task should contain original prompt
    
    # Verify the agent's run method was called
    mock_agent_instance.run.assert_awaited_once()

    # Verify the result from the agent is returned
    assert result == "Task completed successfully."


@pytest.mark.asyncio
@patch('harvester.Agent', new_callable=MagicMock)
async def test_harvester_handles_complex_prompts(mock_agent_class):
    """
    RED: Tests that the Harvester correctly handles complex multi-step prompts.
    """
    # Arrange
    mock_agent_instance = MagicMock()
    mock_agent_instance.run = AsyncMock(return_value="Complex task completed.")
    mock_agent_class.return_value = mock_agent_instance

    harvester = Harvester()
    complex_prompt = "Find AI researchers at YC companies, read their recent posts, and engage thoughtfully with insightful comments"

    # Act
    result = await harvester.harvest(complex_prompt)

    # Assert
    mock_agent_class.assert_called_once()
    call_args = mock_agent_class.call_args
    assert call_args[1]['browser_config']['headless'] is False  # Should be visible for login
    assert complex_prompt in call_args[1]['task']
    
    mock_agent_instance.run.assert_awaited_once()
    assert result == "Complex task completed."


@pytest.mark.asyncio
@patch('harvester.Agent', new_callable=MagicMock)
async def test_harvester_handles_post_fetching_prompts(mock_agent_class):
    """
    RED: Tests that the Harvester correctly handles post-fetching prompts
    and returns structured FetchedPost objects when appropriate.
    """
    # Arrange
    mock_agent_instance = MagicMock()
    
    # Simulate the agent returning structured data for post fetching
    sample_agent_output = [
        {
            "post_id": "urn:li:activity:1",
            "post_url": "https://www.linkedin.com/feed/update/urn:li:activity:1/",
            "author_name": "Author One",
            "author_url": "https://www.linkedin.com/in/authorone/",
            "author_headline": "AI Researcher",
            "content_text": "Latest developments in AI healthcare applications.",
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
            "author_headline": "Healthcare Tech Lead",
            "content_text": "Discussing the future of AI in medical diagnostics.",
            "posted_timestamp_str": "2d",
            "likes_count": 25,
            "comments_count": 8,
            "reposts_count": 3,
            "views_count": 200
        }
    ]
    
    mock_agent_instance.run = AsyncMock(return_value=sample_agent_output)
    mock_agent_class.return_value = mock_agent_instance

    harvester = Harvester()
    fetch_prompt = "Find and extract details from 2 posts about AI in healthcare"

    # Act
    result = await harvester.harvest(fetch_prompt)

    # Assert
    mock_agent_class.assert_called_once()
    call_args = mock_agent_class.call_args
    assert 'LinkedIn.com' in call_args[1]['task']  # Should include LinkedIn navigation
    assert 'logged in' in call_args[1]['task']  # Should include login instructions
    
    mock_agent_instance.run.assert_awaited_once()

    # If result contains structured data, it should be parsed into FetchedPost objects
    if isinstance(result, list) and result and isinstance(result[0], dict):
        # Convert to FetchedPost objects for validation
        posts = [FetchedPost(**post_data) for post_data in result]
        
        assert len(posts) == 2
        assert posts[0].post_id == "urn:li:activity:1"
        assert posts[0].author_name == "Author One"
        assert posts[1].post_id == "urn:li:activity:2"
        assert posts[1].author_name == "Author Two"


@pytest.mark.asyncio  
@patch('harvester.Agent', new_callable=MagicMock)
async def test_harvester_handles_empty_prompt(mock_agent_class):
    """
    RED: Tests that the Harvester validates empty prompts.
    """
    # Arrange
    harvester = Harvester()

    # Act & Assert
    with pytest.raises(ValueError, match="Empty prompt"):
        await harvester.harvest("")
    
    with pytest.raises(ValueError, match="Empty prompt"):
        await harvester.harvest("   ")  # Whitespace only

    with pytest.raises(ValueError, match="Empty prompt"):
        await harvester.harvest(None)

    # Verify no agent was instantiated for invalid prompts
    mock_agent_class.assert_not_called()


@pytest.mark.asyncio
@patch('harvester.Agent', new_callable=MagicMock)
async def test_harvester_returns_string_or_list(mock_agent_class):
    """
    RED: Tests that the Harvester returns appropriate types based on agent output.
    """
    # Arrange
    mock_agent_instance = MagicMock()
    mock_agent_class.return_value = mock_agent_instance

    harvester = Harvester()

    # Test case 1: Agent returns string
    mock_agent_instance.run = AsyncMock(return_value="Action completed successfully")
    result1 = await harvester.harvest("Like posts about blockchain")
    assert isinstance(result1, str)
    assert result1 == "Action completed successfully"

    # Test case 2: Agent returns list (for fetch operations)
    mock_agent_instance.run = AsyncMock(return_value=[{"post_id": "123", "content": "test"}])
    result2 = await harvester.harvest("Fetch posts about machine learning")
    assert isinstance(result2, list)
    assert len(result2) == 1
