"""
Tests for the simplified Flask application.

Tests the new streamlined architecture using PromptTransformer + Harvester
instead of the complex PromptInterpreter + Command approach.
"""

import pytest
import json
from unittest.mock import patch, AsyncMock, MagicMock
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@patch('app.Agent')
@patch('app.PromptTransformer')
def test_process_endpoint_with_simple_prompt(mock_transformer_class, mock_agent_class, client):
    """
    RED: Test the new /api/process endpoint with a simple prompt.
    """
    # Arrange
    mock_transformer = MagicMock()
    mock_transformer.enhance_prompt.return_value = "Enhanced: Like posts about AI"
    mock_transformer_class.return_value = mock_transformer
    
    mock_agent_instance = MagicMock()
    mock_agent_instance.run = AsyncMock(return_value="Successfully liked 5 posts about AI")
    mock_agent_class.return_value = mock_agent_instance
    
    # Act
    response = client.post('/api/process', 
                          data=json.dumps({'prompt': 'Like posts about AI'}),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert 'results' in data
    assert 'enhanced_prompt' in data
    assert 'user_prompt' in data
    assert data['user_prompt'] == 'Like posts about AI'
    assert data['enhanced_prompt'] == 'Enhanced: Like posts about AI'
    assert data['results'] == 'Successfully liked 5 posts about AI'


@patch('app.Agent')
@patch('app.PromptTransformer')
def test_process_endpoint_with_complex_prompt(mock_transformer_class, mock_agent_class, client):
    """
    RED: Test the /api/process endpoint with a complex multi-step prompt.
    """
    # Arrange
    complex_prompt = "Find AI researchers at YC companies and engage thoughtfully"
    enhanced_prompt = f"Enhanced LinkedIn context: {complex_prompt}"
    
    mock_transformer = MagicMock()
    mock_transformer.enhance_prompt.return_value = enhanced_prompt
    mock_transformer_class.return_value = mock_transformer
    
    mock_agent_instance = MagicMock()
    mock_agent_instance.run = AsyncMock(return_value="Engaged with 3 AI researchers")
    mock_agent_class.return_value = mock_agent_instance
    
    # Act
    response = client.post('/api/process',
                          data=json.dumps({'prompt': complex_prompt}),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['user_prompt'] == complex_prompt
    assert data['enhanced_prompt'] == enhanced_prompt
    assert data['results'] == 'Engaged with 3 AI researchers'


@patch('app.Agent')
@patch('app.PromptTransformer')
def test_process_endpoint_with_fetch_posts_prompt(mock_transformer_class, mock_agent_class, client):
    """
    RED: Test the /api/process endpoint with a post-fetching prompt.
    """
    # Arrange
    fetch_prompt = "Find and extract details from posts about blockchain"
    enhanced_prompt = f"LinkedIn context: {fetch_prompt}"
    
    mock_transformer = MagicMock()
    mock_transformer.enhance_prompt.return_value = enhanced_prompt
    mock_transformer_class.return_value = mock_transformer
    
    # Mock agent returning structured post data
    mock_posts_data = [
        {
            "post_id": "urn:li:activity:123",
            "post_url": "https://linkedin.com/feed/update/urn:li:activity:123/",
            "author_name": "Blockchain Expert",
            "author_url": "https://linkedin.com/in/expert/",
            "author_headline": "Crypto Researcher",
            "content_text": "Latest trends in blockchain technology",
            "posted_timestamp_str": "2h",
            "likes_count": 50,
            "comments_count": 10,
            "reposts_count": 5,
            "views_count": 500
        }
    ]
    
    mock_agent_instance = MagicMock()
    mock_agent_instance.run = AsyncMock(return_value=mock_posts_data)
    mock_agent_class.return_value = mock_agent_instance
    
    # Act
    response = client.post('/api/process',
                          data=json.dumps({'prompt': fetch_prompt}),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['user_prompt'] == fetch_prompt
    assert data['enhanced_prompt'] == enhanced_prompt
    assert isinstance(data['results'], list)
    assert len(data['results']) == 1
    assert data['results'][0]['author_name'] == 'Blockchain Expert'


def test_process_endpoint_missing_prompt(client):
    """
    RED: Test the /api/process endpoint with missing prompt.
    """
    # Act
    response = client.post('/api/process',
                          data=json.dumps({}),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Prompt is required' in data['error']


def test_process_endpoint_empty_prompt(client):
    """
    RED: Test the /api/process endpoint with empty prompt.
    """
    # Act
    response = client.post('/api/process',
                          data=json.dumps({'prompt': ''}),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'empty' in data['error'].lower()


@patch('app.Agent')
@patch('app.PromptTransformer')
def test_process_endpoint_handles_agent_errors(mock_transformer_class, mock_agent_class, client):
    """
    RED: Test the /api/process endpoint handles Agent execution errors gracefully.
    """
    # Arrange
    mock_transformer = MagicMock()
    mock_transformer.enhance_prompt.return_value = "Enhanced prompt"
    mock_transformer_class.return_value = mock_transformer
    
    mock_agent_instance = MagicMock()
    mock_agent_instance.run = AsyncMock(side_effect=Exception("Agent execution failed"))
    mock_agent_class.return_value = mock_agent_instance
    
    # Act
    response = client.post('/api/process',
                          data=json.dumps({'prompt': 'Test prompt'}),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 500
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Agent execution failed' in data['error']


@patch('app.PromptTransformer')
def test_process_endpoint_handles_transformer_errors(mock_transformer_class, client):
    """
    RED: Test the /api/process endpoint handles PromptTransformer errors gracefully.
    """
    # Arrange
    mock_transformer = MagicMock()
    mock_transformer.enhance_prompt.side_effect = ValueError("Empty prompt not allowed")
    mock_transformer_class.return_value = mock_transformer
    
    # Act
    response = client.post('/api/process',
                          data=json.dumps({'prompt': '   '}),  # Whitespace prompt
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Empty prompt not allowed' in data['error']


def test_index_endpoint_exists(client):
    """
    RED: Test that the index endpoint still exists and serves the main page.
    """
    # Act
    response = client.get('/')
    
    # Assert
    assert response.status_code == 200


def test_old_endpoints_removed(client):
    """
    RED: Test that old endpoints /api/parse and /api/process_prompt_and_fetch are removed.
    """
    # Act
    parse_response = client.post('/api/parse', 
                               data=json.dumps({'prompt': 'test'}),
                               content_type='application/json')
    
    process_response = client.post('/api/process_prompt_and_fetch',
                                 data=json.dumps({'prompt': 'test'}),
                                 content_type='application/json')
    
    # Assert
    assert parse_response.status_code == 404
    assert process_response.status_code == 404
