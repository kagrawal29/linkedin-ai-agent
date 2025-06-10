# LinkedIn AI Agent

## Purpose
Build a local-first AI agent—powered by Browser Use + OpenAI GPT-4—that autonomously (or with supervision) scrolls your LinkedIn feed, filters posts, researches context, and engages with valuable, human-grade comments, reactions, and messages.

## Project Setup

The initial project structure has been created as per the requirements specification. This includes:
- All Python modules (`interpreter.py`, `harvester.py`, etc.)
- Configuration files (`settings.yaml`, `persona.md`, `filters.yaml`) in the `config/` directory.
- A `requirements.txt` file with initial dependencies.
- A `.gitignore` file for Python projects.

### Next Steps

1.  **Initialize GitHub Repo**: Create a new repository on GitHub and push the initial commit.
2.  **Setup Virtual Environment**: Create and activate a Python virtual environment.
3.  **Install Dependencies**: Run `pip install -r requirements.txt`.

With the setup complete, the project is ready for the implementation of the core features, starting with the `Prompt Interpreter`.

## Project Structure

Here is an overview of the key files and directories in this project:

| File/Directory         | Description                                                                 |
| :--------------------- | :-------------------------------------------------------------------------- |
| `agent.py`             | The main entry point to run the LinkedIn AI Agent.                          |
| `interpreter.py`       | Parses natural language prompts into structured JSON commands for the agent.|
| `harvester.py`         | Launches a browser, scrolls the LinkedIn feed, and extracts post data.      |
| `filter_engine.py`     | Filters extracted posts based on rules defined in `config/filters.yaml`.    |
| `researcher.py`        | Enriches post data with external context using APIs (e.g., DuckDuckGo).     |
| `commenter.py`         | Drafts comments and reactions based on the agent's persona and research.    |
| `executor.py`          | Executes the engagement actions (liking, commenting) in the browser.        |
| `logger.py`            | Handles structured logging of all agent actions for audit and debugging.    |
| `config/`              | A directory containing all configuration files.                             |
| `config/settings.yaml` | General settings for the agent, like API keys and default modes.            |
| `config/persona.md`    | Defines the AI agent's personality, tone, and style.                        |
| `config/filters.yaml`  | Contains the rules for filtering LinkedIn posts.                            |
| `requirements.txt`     | A list of all Python dependencies for the project.                          |
| `.gitignore`           | Specifies which files and directories to exclude from version control.      |
| `README.md`            | This file, containing an overview and documentation for the project.        |
| `SYSTEM_DESIGN.md`     | A detailed description of the system architecture and key modules.          |
| `TASKS.md`             | A task manager to track the project's progress against the roadmap.         |


## 1 · Vision & Objectives

| Goal                     | Description                                                                    | Success KPI                                                        |
| :----------------------- | :----------------------------------------------------------------------------- | :----------------------------------------------------------------- |
| 🧠 Insightful Engagement | Add depth, authenticity, and long-term thinking to LinkedIn conversations.   | ≥ 80 % of agent comments elicit replies / reactions.               |
| ⚙️ Autonomy-to-Supervision Dial | Seamlessly switch between Autonomous and Supervised modes.                   | Mode toggle < 1 sec; zero unintended actions in Supervised mode. |
| 🔒 Privacy & Local Control | Run entirely on Tyler’s machine; no LinkedIn credentials leave the device.     | No outbound traffic containing PII except to OpenAI.               |
| 📜 Transparent Log       | Persist a tamper-proof log of every action for audit & rollback.             | 100 % of actions recorded; searchable in < 200 ms.                 |
