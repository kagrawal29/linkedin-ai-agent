from flask import Flask, request, jsonify, render_template
from interpreter import PromptInterpreter, Command

app = Flask(__name__)
interpreter = PromptInterpreter()

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/api/parse', methods=['POST'])
def parse():
    """Parses the user's prompt and returns the structured command."""
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt is required.'}), 400

    command = interpreter.parse_prompt(prompt)
    # Pydantic models have a .dict() method to convert to a dictionary
    return jsonify(command.dict())

if __name__ == '__main__':
    app.run(debug=True)
