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
- **Chrome CDP Persistent Login Support**: Complete implementation of Chrome DevTools Protocol connection for LinkedIn session reuse
  - `_setup_cdp_connection()`: Connect to user's manually opened Chrome browser via CDP
  - `_setup_fallback_browser()`: Automatic fallback to standalone browser when CDP fails
  - `_get_browser_with_fallback()`: Intelligent browser selection with retry logic
  - `_verify_connection_health()`: Connection health monitoring and validation
  - `_check_chrome_availability()`: Chrome availability checking via `/json/version` endpoint
  - Custom exception types: `CDPConnectionError`, `ChromeNotRunningError`, `ChromeConnectionTimeoutError`
  - Comprehensive logging with emoji status indicators for user clarity
  - `get_connection_status()`: Status information for UI integration
  - `get_chrome_startup_command()`: Helper command for users to start Chrome with correct flags

### Enhanced
- **Robust Error Handling**: Enhanced exception handling with specific error types and user-friendly messages
- **Retry Logic**: Exponential backoff retry mechanism (3 attempts) for transient connection failures
- **User Experience**: Clear logging and status messages throughout CDP connection process
- **Browser Session Management**: Improved browser instance tracking and cleanup

### Technical Improvements
- **TDD Implementation**: Complete RED-GREEN-REFACTOR cycle with 9/9 comprehensive tests passing
- **Exception Compatibility**: Maintained backward compatibility with existing exception types
- **Connection Resilience**: Multiple retry attempts with smart fallback to standalone browser
- **Resource Management**: Proper browser instance cleanup and state tracking

### Documentation
- Updated `TASKS.md` with detailed Phase 4 implementation progress
- Added comprehensive task breakdown for Chrome CDP connection feature
- Documented TDD methodology and implementation approach

### Testing
- Created `tests/test_chrome_cdp_connection.py` with comprehensive test coverage:
  - CDP connection success/failure scenarios
  - Multiple Chrome instance handling
  - User Chrome profile integration
  - Error handling and fallback mechanisms
  - Chrome crash recovery
  - Method existence verification

**Breaking Changes**: None - fully backward compatible
**Dependencies**: Uses existing `browser-use`, `Browser`, `BrowserConfig` classes
**Security**: Manual login required - no automated credential handling

### Added - Phase 3: Debugging and Visibility Enhancements (2024-12-19)

#### ✅ TDD Cycle Completed: Enhanced UI Debugging Capabilities

**New Features:**
- **Transformed Prompt Display**: Flask API now returns both `original_prompt` and `transformed_prompt` for full transparency
- **Agent Action Logging Structure**: Added framework for capturing and displaying agent logs in real-time
- **Structured Post Data Extraction**: Enhanced API to properly extract and serialize LinkedIn post data from agent results
- **Enhanced Error Handling**: Improved error responses with debugging information included

**Frontend Improvements:**
- Added dedicated UI sections for original vs enhanced prompt comparison
- Implemented agent logs display area with structured logging format
- Enhanced post display cards with professional styling and proper data extraction
- Added visual indicators for enhanced prompts (green border highlighting)

**API Enhancements:**
- Updated `/api/process` endpoint with comprehensive debugging response format:
  - `original_prompt`: User's input exactly as entered
  - `transformed_prompt`: Enhanced prompt with LinkedIn guidelines
  - `extracted_posts`: Clean, serializable post data structures
  - `agent_logs`: Framework for real-time agent action logging
  - `status`, `message`, and error handling improvements

**CSS & Styling:**
- Added comprehensive styling for all new debugging UI elements
- Implemented dark theme consistency across prompt displays and agent logs
- Enhanced post cards with hover effects and improved readability
- Added color-coded status indicators for different types of logs and messages

**Technical Implementation:**
- Fixed Flask async compatibility issues by using `asyncio.run()` 
- Implemented proper JSON serialization for complex data structures
- Added HTML escaping for security and proper display
- Created comprehensive test suite for all debugging features (6 new tests)

**Test Coverage:**
- `TestTransformedPromptDisplay`: Tests for API and UI prompt display features
- `TestAgentActionLogging`: Tests for agent logs capture and display structure  
- `TestStructuredDataExtraction`: Tests for post data extraction and serialization
- All tests following strict TDD red-green-refactor methodology

#### ✅ End-to-End Testing Success (2024-12-19)

**Production Validation Completed:**
- **Complete Workflow Tested**: User input → PromptTransformer → Harvester → browser-use Agent → LinkedIn automation
- **Real LinkedIn Automation**: Successfully tested "like first 3 posts on linkedin feed" with full execution
- **Debugging Visibility Verified**: All UI enhancements working perfectly in production

**Bug Fixes Applied:**
- Fixed method name mismatch: `transformer.transform()` → `transformer.enhance_prompt()`
- Fixed JSON serialization issue: AgentHistoryList objects now properly converted to strings
- Ensured Flask server stability with proper error handling

**Validation Results:**
- ✅ PromptTransformer enhancement: "like first 3 posts on linkedin feed" → professional LinkedIn guidelines added
- ✅ Agent execution: Successfully navigated LinkedIn, waited for manual login, executed 3 like actions
- ✅ Debugging output: Full AgentHistoryList with step-by-step execution details displayed
- ✅ UI rendering: All debugging sections populated with real data
- ✅ Success confirmation: "Successfully liked the first three posts on the LinkedIn feed"

**Production Readiness Confirmed:**
- Manual LinkedIn login security feature working correctly
- Professional prompt enhancement maintaining LinkedIn community standards
- Real-time execution logging with detailed DOM element tracking
- Comprehensive error handling and user feedback
- Beautiful, responsive UI with complete debugging visibility

This enhancement significantly improves the developer and user experience by providing full visibility into:
1. How prompts are transformed and enhanced
2. What actions the AI agent is taking step-by-step  
3. What structured data is being extracted from LinkedIn
4. Clear error handling and status reporting

**Files Modified:**
- `app.py`: Enhanced `/api/process` endpoint with debugging response format, fixed method calls and JSON serialization
- `templates/index.html`: Added UI sections for prompts and agent logs
- `static/js/main.js`: Updated JavaScript to handle new API response format
- `static/css/style.css`: Added comprehensive styling for debugging UI elements
- `tests/test_app_debugging.py`: Complete test suite for debugging features

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
