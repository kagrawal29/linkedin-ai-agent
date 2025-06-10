# Changelog

## [0.1.0] - YYYY-MM-DD

### Added
- **Interpreter UI**: Created a simple Flask and JavaScript-based web UI to provide an interactive way to test the `PromptInterpreter`.
- **Prompt Interpreter**: Implemented the `PromptInterpreter` module to parse natural language prompts into structured commands using the OpenAI API.
- **TDD Workflow**: Established a rigorous Test-Driven Development workflow with pytest.
- **Pydantic Models**: Refactored the command structure to use Pydantic for robust, type-safe JSON parsing from the LLM.
- **Environment Management**: Integrated `python-dotenv` for secure management of the OpenAI API key.

### Changed
- Updated the system prompt for the interpreter multiple times to improve reliability and handle ambiguous cases correctly.

### Fixed
- Resolved multiple test failures by refining the system prompt and switching to Pydantic-based response parsing.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2025-06-10

### Added
- **Prompt Interpreter**: Implemented the `PromptInterpreter` class, which uses the OpenAI GPT-4 API to parse natural language prompts into structured `Command` objects. The implementation follows a strict TDD cycle and includes robust error handling and secure API key management via a `.env` file.
- Initial project structure with all modules (`agent.py`, `interpreter.py`, etc.) and configuration files.
- `README.md` with project vision, objectives, and structure.
- `SYSTEM_DESIGN.md` outlining the agent's high-level architecture.
- `TASKS.md` for managing development work with a TDD workflow.
- `.windsurfrules` defining our development principles and best practices.
- `tests/` directory and initial failing test for `interpreter.py` (`tests/test_interpreter.py`).
- `pyproject.toml` to make the project installable for testing.
- `.gitignore` and `requirements.txt` for environment setup.
- Virtual environment `venv` created and dependencies installed.
- `pytest-asyncio` to `requirements.txt` for enabling asynchronous test functions.
- `pytest-dotenv` to `requirements.txt` for automatic loading of `.env` file variables during tests.
- **E2E Browser Testing**: Successfully executed an end-to-end test using `browser-use` to launch a browser, navigate to LinkedIn, and confirm that session cookies can be reused for accessing logged-in pages after a manual login. This validates the core browser automation capability.

### Changed
- **Testing Framework**:
    - Successfully configured the test environment to support `async def` test functions using `pytest-asyncio`.
    - Ensured API keys (e.g., `OPENAI_API_KEY`) are correctly loaded during test runs via `.env` and `pytest-dotenv`.
- **Harvester Module & Tests**:
    - Updated `tests/test_harvester.py`:
        - Aligned `Command` object instantiation with its Pydantic model definition, resolving validation errors.
        - Ensured `test_harvester_executes_like_command` now passes, verifying basic async operation and mocking.
    - Updated `harvester.py`:
        - Modified the `harvest` method to correctly use attributes from the `Command` model (`engagement_type`, `post_limit`) when constructing the natural language task string for the browser agent.
        - Implemented support for "comment" engagement type in `Harvester.harvest`, including a dedicated test case (`test_harvester_executes_comment_command`).
        - Implemented support for "connect" engagement type in `Harvester.harvest`, including a dedicated test case (`test_harvester_executes_connect_command`).
- **Environment Configuration**:
    - Standardized `OPENAI_API_KEY` naming in `.env` to all uppercase for compatibility with the OpenAI client library.
