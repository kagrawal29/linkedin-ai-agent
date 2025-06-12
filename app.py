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
    Simplified endpoint that processes natural language prompts directly.
    
    Uses PromptTransformer to enhance prompts and Harvester to execute them
    via browser-use Agent.
    """
    try:
        # Get and validate prompt
        data = request.get_json()
        user_prompt = data.get('prompt') if data else None
        
        if not user_prompt:
            return jsonify({'error': 'Prompt is required.'}), 400
            
        if user_prompt.strip() == "":
            return jsonify({'error': 'Empty prompt not allowed.'}), 400
        
        # Transform the prompt
        try:
            transformer = PromptTransformer()
            enhanced_prompt = transformer.enhance_prompt(user_prompt)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        # Execute via Harvester
        try:
            harvester = Harvester()
            results = asyncio.run(harvester.harvest(enhanced_prompt))
            
            # Return response
            response_data = {
                'user_prompt': user_prompt,
                'enhanced_prompt': enhanced_prompt,
                'results': results
            }
            
            return jsonify(response_data), 200
            
        except Exception as e:
            logger.exception(f"Error during harvest execution for prompt: '{user_prompt}'")
            return jsonify({'error': f'Agent execution failed: {str(e)}'}), 500
    
    except Exception as e:
        logger.exception(f"Unexpected error in process_prompt endpoint")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
