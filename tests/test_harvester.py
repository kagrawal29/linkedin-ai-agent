from typing import List, Union

import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from harvester import Harvester
from models import FetchedPost


@pytest.mark.asyncio
@patch('harvester.Agent')
async def test_harvester_executes_natural_language_prompt(mock_agent_class):
    """
    RED: Tests that the Harvester correctly passes natural language prompts
    directly to the browser-use Agent without command parsing.
    """
    # Arrange
    harvester = Harvester()
    prompt = "Go to LinkedIn and like 5 posts about AI in healthcare"
    expected_result = "Task completed successfully."
    
    # Mock the Agent
    mock_agent_instance = MagicMock()
    mock_agent_instance.run = AsyncMock(return_value=expected_result)
    mock_agent_class.return_value = mock_agent_instance
    
    # Act
    result = await harvester.harvest(prompt)
    
    # Assert
    mock_agent_class.assert_called_once()
    call_args = mock_agent_class.call_args
    assert call_args[1]['llm'] is not None  # LLM should be passed
    assert prompt in call_args[1]['task']  # Task should contain original prompt
    
    # Verify the agent's run method was called
    mock_agent_instance.run.assert_awaited_once()
    assert result == expected_result


@pytest.mark.asyncio
@patch('harvester.Agent')
async def test_harvester_handles_complex_prompt(mock_agent_class):
    """
    Test that Harvester can handle complex multi-step prompts.
    """
    # Arrange
    harvester = Harvester()
    complex_prompt = "Find AI researchers at YC companies and engage thoughtfully with their posts"
    expected_result = "Engaged with 5 AI researchers from YC companies"
    
    # Mock the Agent
    mock_agent_instance = MagicMock()
    mock_agent_instance.run = AsyncMock(return_value=expected_result)
    mock_agent_class.return_value = mock_agent_instance
    
    # Act
    result = await harvester.harvest(complex_prompt)
    
    # Assert
    mock_agent_class.assert_called_once()
    call_args = mock_agent_class.call_args
    assert call_args[1]['llm'] is not None  # Should have LLM
    assert complex_prompt in call_args[1]['task']
    
    mock_agent_instance.run.assert_awaited_once()
    assert result == expected_result


@pytest.mark.asyncio
@patch('harvester.Agent')
async def test_harvester_handles_fetch_posts_prompt(mock_agent_class):
    """
    Test that Harvester can handle post-fetching prompts and return structured data.
    """
    # Arrange
    harvester = Harvester()
    prompt = "Find and extract details from posts about machine learning"
    
    # Mock structured post data response
    expected_posts = [
        {
            "post_id": "urn:li:activity:123",
            "author_name": "ML Expert",
            "content_text": "Latest advances in machine learning",
            "likes_count": 50
        }
    ]
    
    # Mock the Agent
    mock_agent_instance = MagicMock()
    mock_agent_instance.run = AsyncMock(return_value=expected_posts)
    mock_agent_class.return_value = mock_agent_instance
    
    # Act
    result = await harvester.harvest(prompt)
    
    # Assert
    mock_agent_class.assert_called_once()
    call_args = mock_agent_class.call_args
    assert call_args[1]['llm'] is not None  # Should have LLM
    assert 'LinkedIn.com' in call_args[1]['task']  # Should include LinkedIn navigation
    assert 'logged in' in call_args[1]['task']  # Should include login instructions
    
    mock_agent_instance.run.assert_awaited_once()
    assert result == expected_posts


@pytest.mark.asyncio  
@patch('harvester.Agent')
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
@patch('harvester.Agent')
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
