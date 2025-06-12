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

    # 2. Expected Result (checking individual fields for robustness)
    # The command is invalid because the prompt is missing key details.

    # 3. Execution & Assertion
    actual_command = interpreter.parse_prompt(prompt)
    
    assert actual_command.topic == "AI"
    assert actual_command.post_limit == 0
    assert actual_command.engagement_type == []
    assert actual_command.is_valid is False
    assert isinstance(actual_command.feedback, str) and len(actual_command.feedback) > 0, "Feedback should be a non-empty string for an invalid command"


def test_parse_fetch_posts_prompt():
    """
    RED: Tests that prompts for fetching posts are correctly parsed.
    This includes cases with explicit and implicit post limits.
    """
    interpreter = PromptInterpreter()

    # Case 1: Explicit post limit
    prompt_explicit = "Fetch 3 posts about 'generative AI'"
    expected_command_explicit = Command(
        topic="generative AI",
        post_limit=3,
        engagement_type=["fetch_posts"],
        is_valid=True,
        feedback=""
    )
    actual_command_explicit = interpreter.parse_prompt(prompt_explicit)
    assert actual_command_explicit == expected_command_explicit

    # Case 2: Implicit post limit (should default to 5 for 'fetch_posts')
    prompt_implicit = "Get me articles on 'quantum computing'"
    expected_command_implicit = Command(
        topic="quantum computing",
        post_limit=5, # Assuming system prompt will specify default of 5 for fetch
        engagement_type=["fetch_posts"],
        is_valid=True,
        feedback=""
    )
    actual_command_implicit = interpreter.parse_prompt(prompt_implicit)
    assert actual_command_implicit == expected_command_implicit

