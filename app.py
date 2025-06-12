"""
Simplified Flask application for LinkedIn AI Agent.

Uses the new streamlined architecture: PromptTransformer + Harvester
instead of the complex PromptInterpreter + Command approach.
"""

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env
import os
import asyncio
import logging

from flask import Flask, request, jsonify, render_template
from prompt_transformer import PromptTransformer
from harvester import Harvester
from browser_use import Agent

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')


@app.route('/api/process', methods=['POST'])
def process_prompt():
    """
    Process a natural language prompt through the LinkedIn AI Agent pipeline.
    Now returns detailed debugging information including transformed prompts and agent logs.
    """
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'No prompt provided'}), 400
        
        original_prompt = data['prompt'].strip()
        if not original_prompt:
            return jsonify({'error': 'Empty prompt not allowed'}), 400
        
        # Transform the prompt
        transformer = PromptTransformer()
        transformed_prompt = transformer.transform(original_prompt)
        
        # Handle case where transformation returns None/empty
        if not transformed_prompt:
            transformed_prompt = original_prompt
        
        # Execute the harvesting with transformed prompt using asyncio
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
        
        # Prepare response with debugging information
        response_data = {
            'status': 'success',
            'original_prompt': original_prompt,
            'transformed_prompt': transformed_prompt,
            'result': agent_result if not extracted_posts else f"Successfully processed {len(extracted_posts)} posts",
            'extracted_posts': extracted_posts,
            'agent_logs': agent_logs,
            'message': '✅ Prompt processed successfully with enhanced LinkedIn guidelines'
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        app.logger.error(f"Error during harvest execution for prompt: '{data.get('prompt', 'Unknown')}'")
        app.logger.error(str(e))
        
        # Return error with debugging information
        error_response = {
            'status': 'error',
            'original_prompt': data.get('prompt', ''),
            'transformed_prompt': '',
            'result': '',
            'extracted_posts': [],
            'agent_logs': [],
            'error': f'Processing failed: {str(e)}',
            'message': '❌ Error occurred during processing'
        }
        
        return jsonify(error_response), 500


if __name__ == '__main__':
    app.run(debug=True)
