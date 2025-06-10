# tests/test_interpreter.py
#
# This file contains the unit tests for the Prompt Interpreter.

import pytest
from interpreter import PromptInterpreter, Command

# This test is designed to fail because we have not yet created the
# `PromptInterpreter` class or the `Command` data structure in `interpreter.py`.
# This is the "RED" step in our Test-Driven Development (TDD) cycle.

def test_parse_simple_prompt():
    """
    RED: Tests that a simple, direct prompt can be parsed.
    This will fail until the necessary classes and functions are created.
    """
    # Attempt to import code that does not exist yet.

    # 1. Setup
    # We imagine how we want to use our interpreter.
    interpreter = PromptInterpreter()
    prompt = "Could you comment on 5 recent posts about systems thinking?"

    # 2. Expected Result
    # This is the structured command we expect to get back.
    expected_command = Command(
        topic="systems thinking",
        post_limit=5,
        engagement_type=["comment"],
        is_valid=True,
        feedback=""
    )

    # 3. Execution & Assertion
    # We call the function and check if the output matches our expectation.
    actual_command = interpreter.parse_prompt(prompt)
    assert actual_command == expected_command

def test_parse_ambiguous_prompt():
    """
    RED: Tests that an ambiguous prompt is handled gracefully.
    The interpreter should return an invalid Command with helpful feedback.
    """
    # 1. Setup
    interpreter = PromptInterpreter()
    prompt = "Engage with some posts about AI."

    # 2. Expected Result
    # The command is invalid because the prompt is missing key details.
    expected_command = Command(
        topic="AI",
        post_limit=0,  # Or a default, but 0 indicates it's not set
        engagement_type=[],
        is_valid=False,
        feedback="The prompt is too ambiguous. Please specify the number of posts and the engagement type (e.g., 'like', 'comment')."
    )

    # 3. Execution & Assertion
    actual_command = interpreter.parse_prompt(prompt)
    assert actual_command == expected_command
