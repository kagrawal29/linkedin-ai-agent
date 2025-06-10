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

## [Unreleased]

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
