from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env
import os

from flask import Flask, request, jsonify, render_template
from interpreter import PromptInterpreter, Command
from harvester import Harvester
from models import FetchedPost # For type hinting and .dict()
import asyncio
import logging # Optional: for better error logging

app = Flask(__name__)
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in .env or not loaded correctly by app.py")
interpreter = PromptInterpreter(api_key=openai_api_key)

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/api/parse', methods=['POST'])
def parse_original(): # Renamed to avoid conflict if we want to keep it separate
    """Original endpoint: Parses the user's prompt and returns the structured command."""
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt is required.'}), 400

    command = interpreter.parse_prompt(prompt)
    return jsonify(command.dict())

@app.route('/api/process_prompt_and_fetch', methods=['POST'])
def process_prompt_and_fetch():
    """Processes prompt, and if 'fetch_posts', calls Harvester and returns command + posts_data."""
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt is required.'}), 400

    command_obj = interpreter.parse_prompt(prompt)
    
    posts_data_for_json = None
    harvester_message = None
    error_message = None

    if command_obj.engagement_type == ["fetch_posts"]:
        logger.info(f"Received 'fetch_posts' command for topic: {command_obj.topic}")
        try:
            harvester_instance = Harvester()
            # harvester.harvest is async, so we need to run it in an event loop
            # For Flask, asyncio.run() is a straightforward way to call async from sync code.
            result = asyncio.run(harvester_instance.harvest(command_obj))
            
            if isinstance(result, list):
                if not result: # Empty list is a valid successful result
                    posts_data_for_json = []
                    logger.info("Harvester returned an empty list of posts.")
                elif all(isinstance(item, FetchedPost) for item in result):
                    posts_data_for_json = [post.dict() for post in result]
                    logger.info(f"Successfully fetched {len(posts_data_for_json)} posts.")
                else:
                    error_message = "Harvester returned a list, but items were not in the expected FetchedPost format."
                    logger.error(f"{error_message} Result: {result}")
            elif isinstance(result, str):
                harvester_message = result # This could be a confirmation or an error string from Harvester
                logger.info(f"Harvester returned a string message: {result}")
            else:
                error_message = f"Harvester returned an unexpected data type: {type(result)}"
                logger.error(f"{error_message} Result: {result}")

        except Exception as e:
            logger.exception(f"Error during 'fetch_posts' harvesting process for prompt: '{prompt}'")
            error_message = f"An error occurred while trying to fetch posts: {str(e)}"
    else:
        logger.info(f"Received command type '{command_obj.engagement_type}', Harvester not called.")

    response_payload = {
        'command': command_obj.dict(),
        'posts_data': posts_data_for_json,
        'harvester_message': harvester_message,
        'error': error_message
    }
    return jsonify(response_payload)

if __name__ == '__main__':
    app.run(debug=True)
