# Task Manager

This document tracks the project's tasks based on the 1-week sprint plan.

## 1-Week Sprint Plan

| Day     | Deliverable                                         | Status      |
| :------ | :-------------------------------------------------- | :---------- |
| **Day 1** | Repo scaffold, env setup, Prompt Interpreter done.  | ⏳ In Progress |
| **Day 2** | Feed Harvester + basic extraction.                  | 📋 To Do     |
| **Day 3** | Filtering engine, logging stub.                     | 📋 To Do     |
| **Day 4** | Research & Comment draft; CLI preview.              | 📋 To Do     |
| **Day 5** | Engagement Executor (like, comment) + supervised UI.| 📋 To Do     |
| **Day 6** | Autonomous flow, full logging, unit tests.          | 📋 To Do     |
| **Day 7** | Hardening, risk mitigations, README with usage steps.| 📋 To Do     |

### Task Breakdown (TDD Workflow)

#### Day 1: Scaffolding & Prompt Interpreter
- [x] Create project directory and file structure.
- [x] Initialize Git and push to a new GitHub repository.
- [x] Set up a Python virtual environment and install dependencies.
- [x] Create `SYSTEM_DESIGN.md`, `TASKS.md`, and `WINDSURF_RULES.md`.
- [x] Architect the System: Populate all Python modules with high-level, plain English comments.
- [x] Setup `tests/` directory for Test-Driven Development.

- [ ] **Implement `interpreter.py`**
    - [ ] **1. RED**: Write a failing test for `parse_prompt` in `tests/test_interpreter.py` for a simple, clear prompt.
    - [ ] **2. GREEN**: Write the simplest code in `interpreter.py` to make the test pass.
    - [ ] **3. REFACTOR**: Improve the `parse_prompt` function.
    - [ ] **4. RED**: Write a failing test for handling ambiguous prompts.
    - [ ] **5. GREEN**: Add logic to `parse_prompt` to handle ambiguity.
    - [ ] **6. REFACTOR**: Improve the ambiguity-handling code.

#### Day 2: Feed Harvester
- [ ] **Implement `harvester.py`**
    - [ ] **1. RED**: Write a test in `tests/test_harvester.py` to check browser launch (mocked).
    - [ ] **2. GREEN**: Write code in `harvester.py` to launch a browser.
    - [ ] **3. REFACTOR**: Improve browser launch code.
    - [ ] **4. RED**: Write a test for `scroll_and_extract` using mock HTML data.
    - [ ] **5. GREEN**: Implement the `scroll_and_extract` method to parse the mock data.
    - [ ] **6. REFACTOR**: Clean up the harvesting logic.

#### Day 3: Filtering Engine & Logging Stub
- [ ] **Implement `filter_engine.py`**
    - [ ] **1. RED**: Write a test in `tests/test_filter_engine.py` with mock posts and rules; test that it correctly filters by keyword.
    - [ ] **2. GREEN**: Write simple code in `filter_engine.py` to filter by keyword.
    - [ ] **3. REFACTOR**: Improve the keyword filtering logic.
    - [ ] **4. RED**: Add tests for all other filter types (likes, comments, content type).
    - [ ] **5. GREEN**: Implement the remaining filter logic.
    - [ ] **6. REFACTOR**: Finalize the `apply_filters` function.
- [ ] **Implement `logger.py` Stub**
    - [ ] **1. RED**: Write a test in `tests/test_logger.py` to check if a log file is created and a message is written.
    - [ ] **2. GREEN**: Write a simple `Logger` class that creates a file and writes a string to it.
    - [ ] **3. REFACTOR**: Improve the basic logging mechanism.

#### Day 4: Research & Comment Draft
- [ ] **Implement `researcher.py`**
    - [ ] **1. RED**: Write a test in `tests/test_researcher.py` to check if the `enrich_post` function returns a summary (mocking the LLM call).
    - [ ] **2. GREEN**: Implement the basic `enrich_post` function structure.
    - [ ] **3. REFACTOR**: Improve the summarization logic.
- [ ] **Implement `commenter.py`**
    - [ ] **1. RED**: Write a test in `tests/test_commenter.py` to check if `draft_comment` returns a string (mocking the LLM call).
    - [ ] **2. GREEN**: Implement the `draft_comment` function to call the mocked LLM and return its text.
    - [ ] **3. REFACTOR**: Improve the comment drafting logic, ensuring it uses the persona.

#### Day 5: Engagement Executor & Supervised UI
- [ ] **Implement `executor.py`**
    - [ ] **1. RED**: Write tests in `tests/test_executor.py` for `like` and `comment` methods, checking if they would interact with a mock browser object.
    - [ ] **2. GREEN**: Implement the `like` and `comment` methods to call the mock browser's methods.
    - [ ] **3. REFACTOR**: Clean up the executor code.
- [ ] **Implement Supervised UI in `agent.py`**
    - [ ] **1. RED**: Write a test to check if the agent presents a drafted comment and correctly interprets user input (e.g., 'P' for post).
    - [ ] **2. GREEN**: Add the `input()` prompt and conditional logic to `agent.py`.
    - [ ] **3. REFACTOR**: Improve the supervised mode user interface.

#### Day 6: Autonomous Flow & Full Logging
- [ ] **Integrate Autonomous Flow in `agent.py`**
    - [ ] **1. RED**: Write an end-to-end integration test that runs the full agent pipeline (with all external calls mocked) and checks if the executor's methods are called in autonomous mode.
    - [ ] **2. GREEN**: Connect all the modules in `agent.py` to create the full pipeline.
    - [ ] **3. REFACTOR**: Clean up the main agent orchestration logic.
- [ ] **Expand `logger.py`**
    - [ ] **1. RED**: Write a test to ensure logs are written in a structured JSONL format.
    - [ ] **2. GREEN**: Update the `Logger` to write in the JSONL format.
    - [ ] **3. REFACTOR**: Improve the logging output and structure.

#### Day 7: Hardening & Documentation
- [ ] **Error Handling**: Go through each module and add `try...except` blocks for anticipated issues (e.g., network errors, parsing failures).
- [ ] **Unit Test Coverage**: Review test coverage and add more unit tests for edge cases.
- [ ] **Update `README.md`**: Add final usage instructions, a guide on how to run the agent, and a description of the configuration files.
- [ ] **Final Code Review**: Read through the entire codebase to ensure it meets the standards defined in `WINDSURF_RULES.md`.
