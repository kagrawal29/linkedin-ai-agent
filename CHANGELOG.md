# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2025-06-12

### 🚀 MAJOR ARCHITECTURAL TRANSITION - In Progress
**Vision**: Transitioning from constrained interpreter to flexible, natural language AI agent leveraging browser-use's full capabilities.

#### ✅ Phase 0: Constrained Interpreter (COMPLETED)
- **Prompt Interpreter**: Full implementation with OpenAI structured parsing
- **Harvester Integration**: Working browser-use Agent integration with task conversion
- **Flask UI**: Dual endpoints (`/api/parse`, `/api/process_prompt_and_fetch`) with post display
- **Test Coverage**: Comprehensive TDD coverage for interpreter and harvester modules
- **FetchedPost Model**: Structured post data parsing with Pydantic validation
- **Environment Fixes**: Resolved API key loading and environment variable issues

#### 🔄 Phase 1: Architecture Transition (IN PROGRESS)
- **PromptTransformer**: ✅ Complete RED-GREEN-REFACTOR cycle with full test coverage
- **Harvester Simplification**: ✅ Direct natural language prompt handling (removed Command objects)
- **Flask App Migration**: ✅ Single `/api/process` endpoint with streamlined flow
- **Test Migration**: ✅ All tests rewritten for string-based prompts vs structured commands

### Added
- **Architectural Transition Plan**: Comprehensive 4-phase plan in `TASKS.md`
  - Phase 1: Architecture Transition (PromptTransformer)
  - Phase 2: Enhanced Capabilities & Safety
  - Phase 3: Testing & Optimization  
  - Phase 4: Documentation & Deployment
- **Success Metrics**: Quantifiable goals (50% code reduction, 40% fewer API calls, 70% fewer rate limits)
- **Rollback Plan**: Safety mechanisms for reverting changes if issues arise
- **Git Workflow**: Feature branch `feature/prompt-transformer-transition` for transition work
- **PromptTransformer Module**: New flexible prompt enhancement system replacing constrained interpreter
- **Simplified Flask App**: New `/api/process` endpoint integrating PromptTransformer + Harvester

### Changed
- **Development Methodology**: Strict TDD (RED-GREEN-REFACTOR) maintained throughout transition
- **Architecture Vision**: From engagement-type-limited system to general-purpose AI agent
- **Harvester Module**: Simplified to accept natural language strings instead of Command objects
- **Test Strategy**: All tests updated to use proper mocking to prevent unwanted browser automation

### Fixed
- **🔧 CRITICAL: Prevented Unwanted Browser Automation During Tests** (2025-06-12)
  - **Issue**: Tests were accidentally launching real browsers and navigating to random websites (x.com, facebook.com) 
  - **Root Cause**: Tests were patching `@patch('app.Agent')` but Agent is created inside `Harvester.__init__()`
  - **Solution**: Fixed mocking to `@patch('harvester.Agent')` to patch where Agent is actually instantiated
  - **Impact**: All 9 Flask app tests now pass without unwanted browser launches, TDD workflow can continue safely
- **🔑 CRITICAL: Added Persistent Browser Sessions for LinkedIn Login** (2025-06-12)
  - **Issue**: Browser opens LinkedIn but user not logged in → Agent gets stuck waiting
  - **Root Cause**: Each browser session starts fresh without saved login state
  - **Solution**: Implemented persistent user data directory (`~/.linkedin_ai_agent/browser_data/`)
  - **Impact**: 
    - First run: User logs in manually, session is saved automatically
    - Future runs: Browser loads saved session → Already logged in
    - Added helper methods: `clear_browser_data()`, `is_browser_data_present()`
    - Enhanced prompts with LinkedIn-specific navigation instructions

### Added
- **Architectural Transition Plan**: Comprehensive 4-phase plan in `TASKS.md`
  - Phase 1: Architecture Transition (PromptTransformer)
  - Phase 2: Enhanced Capabilities & Safety
  - Phase 3: Testing & Optimization  
  - Phase 4: Documentation & Deployment
- **Success Metrics**: Quantifiable goals (50% code reduction, 40% fewer API calls, 70% fewer rate limits)
- **Rollback Plan**: Safety mechanisms for reverting changes if issues arise
- **Git Workflow**: Feature branch `feature/prompt-transformer-transition` for transition work

### Changed
- **Development Methodology**: Strict TDD (RED-GREEN-REFACTOR) maintained throughout transition
- **Architecture Vision**: From engagement-type-limited system to general-purpose AI agent

---

## [0.1.5] - 2024-12-12

### 🎉 MAJOR MILESTONE: End-to-End Demo Success
- **Achievement**: Complete LinkedIn AI Agent workflow now functional from UI to browser automation
- **Tested Workflow**: Flask UI → PromptTransformer → Harvester → browser-use Agent → LinkedIn automation
- **User Experience**: Simple natural language input → professional LinkedIn automation
- **Security**: Manual login required (secure by design)
- **Technical Status**: All components integrated and working together

### Verified Components
- **Frontend**: HTML form → JavaScript → Flask API call working
- **Backend**: Flask `/api/process` → PromptTransformer → Harvester → browser-use Agent
- **Browser Automation**: Real browser launch, LinkedIn navigation, login detection
- **Demo Test**: "Go to LinkedIn and find 3 posts about artificial intelligence" - SUCCESS

## [0.1.4] - 2024-12-12

### Fixed
- **Critical Fix: Browser-use API Compatibility**
  - **Issue**: Import errors with `BrowserSession` and incorrect browser configuration parameters causing test failures and runtime errors
  - **Root Cause**: Using outdated browser-use API documentation that referenced `BrowserSession` class not available in current version (0.1.41)
  - **Solution**: 
    - Simplified harvester to use basic `Agent(task, llm)` configuration without complex browser setup
    - Removed dependency on `BrowserSession`, `Browser`, and `BrowserConfig` classes
    - Updated all tests to verify correct Agent initialization with simplified parameters
    - Maintained LinkedIn-specific prompt enhancement and error handling
  - **Impact**: All harvester tests now pass (5/5), basic browser automation functionality restored
  - **Next Steps**: Will add persistent browser sessions using correct API once end-to-end functionality is confirmed

### Technical Details
- Removed imports: `BrowserSession`, `Browser`, `BrowserConfig` from harvester.py
- Simplified `Harvester.__init__()` to only initialize LLM and data directory
- Updated `harvest()` method to create `Agent(task=enhanced_prompt, llm=self.llm)`
- Fixed all test assertions to check for `llm` parameter instead of browser-related parameters
- Preserved helper methods for future persistence implementation

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

## [Unreleased] - 2025-06-10

### Added
- Enhanced `PromptInterpreter` to recognize and parse "fetch_posts" commands, including default post limits (Sub-Task 6.B.2.1).
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
- **Feed Harvester - Post Fetching**:
  - Implemented `fetch_posts` engagement type in `Harvester.harvest` to retrieve structured post data from LinkedIn.
  - Introduced `FetchedPost` Pydantic model in `models.py` to define the structure of fetched LinkedIn posts.
  - Added TDD tests for `fetch_posts`, ensuring correct agent interaction and parsing of post data into `FetchedPost` objects.

### Changed
- **Testing Framework**:
    - Successfully configured the test environment to support `async def` test functions using `pytest-asyncio`.
    - Ensured API keys (e.g., `OPENAI_API_KEY`) are correctly loaded during test runs via `.env` and `pytest-dotenv`.
- **Harvester Module & Tests**:
    - Updated `harvester.py`:
        - Modified the `harvest` method to correctly use attributes from the `Command` model (`engagement_type`, `post_limit`) when constructing the natural language task string for the browser agent.
        - Implemented support for "comment" engagement type, including a dedicated test case.
        - Implemented support for "connect" engagement type, including a dedicated test case.
        - Refactored `Harvester.harvest` method:
            - Return type is now `Union[List[FetchedPost], str]` to support both structured post data and string confirmations for other engagement types.
            - Updated `Agent` interaction to pass the task as a keyword argument to `agent.run(task=...)` instead of the `Agent` constructor.
    - Updated `tests/test_harvester.py`:
        - Aligned `Command` object instantiation with its Pydantic model definition, resolving validation errors.
        - Ensured `test_harvester_executes_like_command` now passes, verifying basic async operation and mocking.
        - Updated all tests to align with the new agent call pattern and `harvest` method return types, ensuring all tests pass.
- **Environment Configuration**:
    - Standardized `OPENAI_API_KEY` naming in `.env` to all uppercase for compatibility with the OpenAI client library.
