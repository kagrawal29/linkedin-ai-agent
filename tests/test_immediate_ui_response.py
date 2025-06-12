"""
Tests for immediate UI response functionality.

Tests the new API endpoints for immediate enhanced prompt delivery:
- /api/enhance: Returns enhanced prompt immediately
- /api/execute: Executes pre-enhanced prompts 
- /api/process: Modified to support immediate vs delayed execution modes
"""

import pytest
import json
import asyncio
from unittest.mock import patch, MagicMock
from app import app


class TestImmediateUIResponse:
    """Test cases for immediate enhanced prompt delivery to UI."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_enhance_endpoint_returns_immediate_response(self):
        """RED: Test /api/enhance returns enhanced prompt immediately."""
        prompt_data = {
            'prompt': 'Like 3 posts about AI',
            'use_templates': True,
            'use_llm': False
        }
        
        response = self.app.post('/api/enhance', 
                                data=json.dumps(prompt_data),
                                content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Should return enhanced prompt immediately
        assert data['status'] == 'enhanced'
        assert data['original_prompt'] == 'Like 3 posts about AI'
        assert data['transformed_prompt'] != data['original_prompt']
        assert len(data['transformed_prompt']) > len(data['original_prompt'])
        assert 'LinkedIn' in data['transformed_prompt']
        assert data['use_templates'] == True
        assert data['use_llm'] == False
        assert '✅' in data['message']
    
    def test_enhance_endpoint_with_llm_integration(self):
        """RED: Test /api/enhance with LLM-powered enhancement."""
        prompt_data = {
            'prompt': 'Comment thoughtfully on AI startup posts',
            'use_templates': True,
            'use_llm': True
        }
        
        response = self.app.post('/api/enhance', 
                                data=json.dumps(prompt_data),
                                content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Should handle LLM integration
        assert data['status'] == 'enhanced'
        assert data['use_llm'] == True
        assert data['transformed_prompt'] != data['original_prompt']
    
    def test_enhance_endpoint_error_handling(self):
        """RED: Test /api/enhance error handling for invalid inputs."""
        # Test missing prompt
        response = self.app.post('/api/enhance', 
                                data=json.dumps({}),
                                content_type='application/json')
        assert response.status_code == 400
        
        # Test empty prompt
        response = self.app.post('/api/enhance', 
                                data=json.dumps({'prompt': ''}),
                                content_type='application/json')
        assert response.status_code == 400
        
        # Test whitespace-only prompt
        response = self.app.post('/api/enhance', 
                                data=json.dumps({'prompt': '   '}),
                                content_type='application/json')
        assert response.status_code == 400
    
    def test_process_endpoint_immediate_mode(self):
        """RED: Test /api/process with execute_immediately=False returns prompt immediately."""
        prompt_data = {
            'prompt': 'Find 5 posts about startups',
            'execute_immediately': False,
            'use_templates': True
        }
        
        response = self.app.post('/api/process', 
                                data=json.dumps(prompt_data),
                                content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Should return enhanced prompt immediately without execution
        assert data['status'] == 'enhanced_ready'
        assert data['execution_mode'] == 'ready'
        assert data['transformed_prompt'] != data['original_prompt']
        assert data['result'] == ''
        assert data['extracted_posts'] == []
        assert '✅' in data['message']
    
    @patch('app.Harvester')
    def test_process_endpoint_immediate_execution_mode(self, mock_harvester_class):
        """RED: Test /api/process with execute_immediately=True executes and returns results."""
        # Mock harvester with simple return value
        mock_harvester = MagicMock()
        
        async def mock_harvest(prompt):
            return [
                {
                    'post_id': 'test123',
                    'author_name': 'Test User',
                    'content_text': 'Great AI insights!',
                    'likes_count': 42
                }
            ]
        
        mock_harvester.harvest = mock_harvest
        mock_harvester_class.return_value = mock_harvester
        
        prompt_data = {
            'prompt': 'Like posts about AI',
            'execute_immediately': True,
            'use_templates': True
        }
        
        response = self.app.post('/api/process', 
                                data=json.dumps(prompt_data),
                                content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Should execute immediately and return complete results
        assert data['status'] == 'completed'
        assert data['execution_mode'] == 'immediate'
        assert data['transformed_prompt'] != data['original_prompt']
        assert len(data['extracted_posts']) > 0
        assert data['extracted_posts'][0]['post_id'] == 'test123'
    
    @patch('app.Harvester')
    def test_execute_endpoint_runs_pre_enhanced_prompt(self, mock_harvester_class):
        """RED: Test /api/execute runs a pre-enhanced prompt successfully."""
        # Mock harvester with simple return value
        mock_harvester = MagicMock()
        
        async def mock_harvest(prompt):
            return ["Execution completed successfully"]
        
        mock_harvester.harvest = mock_harvest
        mock_harvester_class.return_value = mock_harvester
        
        execution_data = {
            'original_prompt': 'Like AI posts',
            'enhanced_prompt': '''You are working on LinkedIn...
            
Task: Like AI posts

Detailed execution plan:
1. Navigate to LinkedIn feed
2. Search for posts about AI
3. Like relevant posts

Important guidelines:
- Maintain professional tone'''
        }
        
        response = self.app.post('/api/execute', 
                                data=json.dumps(execution_data),
                                content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Should execute the enhanced prompt
        assert data['status'] == 'executed'
        assert data['original_prompt'] == 'Like AI posts'
        assert 'LinkedIn' in data['enhanced_prompt']
        assert 'Execution completed successfully' in data['result']
    
    def test_execute_endpoint_error_handling(self):
        """RED: Test /api/execute error handling for invalid inputs."""
        # Test missing enhanced_prompt
        response = self.app.post('/api/execute', 
                                data=json.dumps({}),
                                content_type='application/json')
        assert response.status_code == 400
        
        # Test empty enhanced_prompt
        response = self.app.post('/api/execute', 
                                data=json.dumps({'enhanced_prompt': ''}),
                                content_type='application/json')
        assert response.status_code == 400
    
    def test_response_time_immediate_enhancement(self):
        """RED: Test that enhancement response is immediate (< 2 seconds for simple prompts)."""
        import time
        
        prompt_data = {
            'prompt': 'Like posts about technology',
            'use_templates': False,  # Use faster generic enhancement
            'use_llm': False
        }
        
        start_time = time.time()
        response = self.app.post('/api/enhance', 
                                data=json.dumps(prompt_data),
                                content_type='application/json')
        response_time = time.time() - start_time
        
        assert response.status_code == 200
        assert response_time < 2.0, f"Enhancement took {response_time:.2f}s, should be < 2s"
        
        data = json.loads(response.data)
        assert data['status'] == 'enhanced'
    
    @patch('app.Harvester')
    def test_workflow_enhance_then_execute(self, mock_harvester_class):
        """RED: Test complete workflow: enhance -> get enhanced prompt -> execute."""
        # Step 1: Enhance prompt
        enhance_data = {
            'prompt': 'Connect with 3 AI researchers',
            'use_templates': True,
            'use_llm': False
        }
        
        enhance_response = self.app.post('/api/enhance', 
                                        data=json.dumps(enhance_data),
                                        content_type='application/json')
        
        assert enhance_response.status_code == 200
        enhance_result = json.loads(enhance_response.data)
        assert enhance_result['status'] == 'enhanced'
        
        # Step 2: Execute enhanced prompt
        mock_harvester = MagicMock()
        
        async def mock_harvest(prompt):
            return ["Connected successfully"]
        
        mock_harvester.harvest = mock_harvest
        mock_harvester_class.return_value = mock_harvester
        
        execute_data = {
            'original_prompt': enhance_result['original_prompt'],
            'enhanced_prompt': enhance_result['transformed_prompt']
        }
        
        execute_response = self.app.post('/api/execute', 
                                        data=json.dumps(execute_data),
                                        content_type='application/json')
        
        assert execute_response.status_code == 200
        execute_result = json.loads(execute_response.data)
        assert execute_result['status'] == 'executed'
        assert execute_result['original_prompt'] == 'Connect with 3 AI researchers'
    
    def test_template_integration_in_immediate_response(self):
        """RED: Test that template enhancement is included in immediate response."""
        prompt_data = {
            'prompt': 'Like 5 posts about machine learning from Google employees',
            'use_templates': True,
            'use_llm': False
        }
        
        response = self.app.post('/api/enhance', 
                                data=json.dumps(prompt_data),
                                content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Should include template-enhanced content
        enhanced_prompt = data['transformed_prompt']
        assert 'LinkedIn' in enhanced_prompt
        assert 'Task:' in enhanced_prompt
        assert 'Detailed execution plan:' in enhanced_prompt
        assert 'Navigate to LinkedIn' in enhanced_prompt
        assert 'guidelines:' in enhanced_prompt
        
        # Should preserve original parameters
        assert '5' in enhanced_prompt
        assert 'machine learning' in enhanced_prompt.lower()
        assert 'Google' in enhanced_prompt
