"""
Flask web application for LinkedIn AI Agent.

Uses the new streamlined architecture: PromptTransformer + Harvester
with immediate enhanced prompt delivery and background execution.
"""

import asyncio
import threading
from flask import Flask, request, jsonify, render_template

from prompt_transformer import PromptTransformer
from harvester import Harvester

app = Flask(__name__)

# Global storage for ongoing executions (in production, use Redis or similar)
execution_status = {}
execution_results = {}

@app.route('/')
def index():
    """Serve the main application page."""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'LinkedIn AI Agent is running'}), 200

@app.route('/api/enhance', methods=['POST'])
def enhance_prompt():
    """
    NEW: Immediate prompt enhancement endpoint.
    Returns enhanced prompt immediately without executing the harvesting.
    """
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'No prompt provided'}), 400
        
        original_prompt = data['prompt'].strip()
        if not original_prompt:
            return jsonify({'error': 'Empty prompt not allowed'}), 400
        
        # Get template and LLM preferences
        # Disable template-based enhancement by default to use sophisticated browser-automation enhancer
        use_templates = data.get('use_templates', False)
        use_llm = data.get('use_llm', False)
        
        # Transform the prompt immediately
        transformer = PromptTransformer(use_templates=use_templates, use_llm=use_llm)
        transformed_prompt = transformer.enhance_prompt(original_prompt)
        
        # Handle case where transformation returns None/empty
        if not transformed_prompt:
            transformed_prompt = original_prompt
        
        # Return immediately with enhanced prompt
        response_data = {
            'status': 'enhanced',
            'original_prompt': original_prompt,
            'transformed_prompt': transformed_prompt,
            'use_templates': use_templates,
            'use_llm': use_llm,
            'message': '✅ Prompt enhanced successfully - ready for execution'
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        app.logger.error(f"Error during prompt enhancement: '{data.get('prompt', 'Unknown')}'")
        app.logger.error(str(e))
        
        error_response = {
            'status': 'error',
            'original_prompt': data.get('prompt', ''),
            'transformed_prompt': '',
            'error': f'Enhancement failed: {str(e)}',
            'message': '❌ Error occurred during prompt enhancement'
        }
        
        return jsonify(error_response), 500

@app.route('/api/process', methods=['POST'])
def process_prompt():
    """
    MODIFIED: Process a natural language prompt with immediate enhanced prompt response.
    Now returns enhanced prompt immediately and continues execution in background.
    """
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'No prompt provided'}), 400
        
        original_prompt = data['prompt'].strip()
        if not original_prompt:
            return jsonify({'error': 'Empty prompt not allowed'}), 400
        
        # Get execution preferences
        execute_immediately = data.get('execute_immediately', False)
        # Disable template-based enhancement by default to use sophisticated browser-automation enhancer
        use_templates = data.get('use_templates', False)
        use_llm = data.get('use_llm', False)
        
        # Transform the prompt immediately
        transformer = PromptTransformer(use_templates=use_templates, use_llm=use_llm)
        transformed_prompt = transformer.enhance_prompt(original_prompt)
        
        # Handle case where transformation returns None/empty
        if not transformed_prompt:
            transformed_prompt = original_prompt
        
        if execute_immediately:
            # Execute harvesting immediately (blocking)
            harvester = Harvester()
            agent_result = asyncio.run(harvester.harvest(transformed_prompt))
            
            # Extract structured posts if result is a list of dictionaries
            extracted_posts = []
            if isinstance(agent_result, list) and agent_result and isinstance(agent_result[0], dict):
                # Filter to only include serializable post data
                for item in agent_result:
                    if isinstance(item, dict):
                        # Clean the dictionary to ensure JSON serialization
                        clean_post = {
                            'post_id': item.get('post_id', ''),
                            'author_name': item.get('author_name', ''),
                            'content_text': item.get('content_text', ''),
                            'likes_count': item.get('likes_count', 0),
                            'author_url': item.get('author_url', ''),
                            'post_url': item.get('post_url', ''),
                            'posted_timestamp_str': item.get('posted_timestamp_str', '')
                        }
                        extracted_posts.append(clean_post)
            
            # TODO: Implement agent logs capture (for future enhancement)
            agent_logs = []
            
            # Return complete result
            response_data = {
                'status': 'completed',
                'original_prompt': original_prompt,
                'transformed_prompt': transformed_prompt,
                'result': str(agent_result) if agent_result else "No result returned",
                'extracted_posts': extracted_posts,
                'agent_logs': agent_logs,
                'execution_mode': 'immediate',
                'message': '✅ Prompt processed and executed successfully'
            }
            
        else:
            # Return enhanced prompt immediately, execution can be triggered separately
            response_data = {
                'status': 'enhanced_ready',
                'original_prompt': original_prompt,
                'transformed_prompt': transformed_prompt,
                'result': '',
                'extracted_posts': [],
                'agent_logs': [],
                'execution_mode': 'ready',
                'use_templates': use_templates,
                'use_llm': use_llm,
                'message': '✅ Prompt enhanced and ready for execution'
            }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        app.logger.error(f"Error during prompt processing: '{data.get('prompt', 'Unknown')}'")
        app.logger.error(str(e))
        
        # Return error with debugging information
        error_response = {
            'status': 'error',
            'original_prompt': data.get('prompt', ''),
            'transformed_prompt': '',
            'result': '',
            'extracted_posts': [],
            'agent_logs': [],
            'execution_mode': 'failed',
            'error': f'Processing failed: {str(e)}',
            'message': '❌ Error occurred during processing'
        }
        
        return jsonify(error_response), 500

@app.route('/api/execute', methods=['POST'])
def execute_enhanced_prompt():
    """
    NEW: Execute a pre-enhanced prompt.
    Designed to work with prompts enhanced via /api/enhance endpoint.
    """
    try:
        data = request.get_json()
        if not data or 'enhanced_prompt' not in data:
            return jsonify({'error': 'No enhanced prompt provided'}), 400
        
        enhanced_prompt = data['enhanced_prompt'].strip()
        if not enhanced_prompt:
            return jsonify({'error': 'Empty enhanced prompt not allowed'}), 400
        
        original_prompt = data.get('original_prompt', enhanced_prompt)
        
        # Execute the harvesting with enhanced prompt
        harvester = Harvester()
        agent_result = asyncio.run(harvester.harvest(enhanced_prompt))
        
        # Extract structured posts if result is a list of dictionaries
        extracted_posts = []
        if isinstance(agent_result, list) and agent_result and isinstance(agent_result[0], dict):
            # Filter to only include serializable post data
            for item in agent_result:
                if isinstance(item, dict):
                    # Clean the dictionary to ensure JSON serialization
                    clean_post = {
                        'post_id': item.get('post_id', ''),
                        'author_name': item.get('author_name', ''),
                        'content_text': item.get('content_text', ''),
                        'likes_count': item.get('likes_count', 0),
                        'author_url': item.get('author_url', ''),
                        'post_url': item.get('post_url', ''),
                        'posted_timestamp_str': item.get('posted_timestamp_str', '')
                    }
                    extracted_posts.append(clean_post)
        
        # TODO: Implement agent logs capture (for future enhancement)
        agent_logs = []
        
        # Prepare response with execution results
        response_data = {
            'status': 'executed',
            'original_prompt': original_prompt,
            'enhanced_prompt': enhanced_prompt,
            'result': str(agent_result) if agent_result else "No result returned",
            'extracted_posts': extracted_posts,
            'agent_logs': agent_logs,
            'message': '✅ Enhanced prompt executed successfully'
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        app.logger.error(f"Error during enhanced prompt execution")
        app.logger.error(str(e))
        
        # Return error with debugging information
        error_response = {
            'status': 'error',
            'original_prompt': data.get('original_prompt', ''),
            'enhanced_prompt': data.get('enhanced_prompt', ''),
            'result': '',
            'extracted_posts': [],
            'agent_logs': [],
            'error': f'Execution failed: {str(e)}',
            'message': '❌ Error occurred during execution'
        }
        
        return jsonify(error_response), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
