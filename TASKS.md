# Task Manager

This document tracks the project's tasks for transitioning from a constrained interpreter to a general-purpose AI agent architecture.

## **ARCHITECTURAL TRANSITION SPRINT PLAN**

**Vision:** Transform from engagement-type-limited system to flexible, natural language AI agent leveraging browser-use's full capabilities.

**Methodology:** Strict TDD (RED-GREEN-REFACTOR) with continuous functionality validation.

| Phase | Deliverable | Duration | Status |
|:------|:-----------|:---------|:-------|
| **Phase 1** | Architecture Transition (PromptTransformer) | Days 1-2 | 📋 Planned |
| **Phase 2** | Enhanced Capabilities & Safety | Days 3-4 | 📋 Planned |
| **Phase 3** | Testing & Optimization | Days 5-6 | 📋 Planned |
| **Phase 4** | Documentation & Deployment | Day 7 | 📋 Planned |

---

## **COMPLETED WORK (Previous Architecture)**

### ✅ Day 1-2: Foundation & Constrained Interpreter
- [x] **Project Setup**
  - [x] Repository scaffolding, environment setup
  - [x] Git initialization and GitHub repository
  - [x] Python virtual environment and dependencies
  - [x] Documentation structure (`SYSTEM_DESIGN.md`, `CHANGELOG.md`, `.windsurfrules`)

- [x] **Constrained Interpreter Implementation (TDD)**
  - [x] **RED**: Failing tests for structured command parsing
  - [x] **GREEN**: `PromptInterpreter` class with OpenAI structured parsing
  - [x] **REFACTOR**: System prompt for engagement type validation
  - [x] **Command** model with engagement type constraints (`like`, `comment`, `share`, `fetch_posts`)

- [x] **Harvester Integration (TDD)**
  - [x] **RED**: Failing tests for browser-use integration
  - [x] **GREEN**: Command-to-task conversion logic
  - [x] **REFACTOR**: FetchedPost model and parsing logic

- [x] **Flask UI Implementation**
  - [x] Basic web interface with prompt input
  - [x] Dual endpoints: `/api/parse` and `/api/process_prompt_and_fetch`
  - [x] Post display functionality

- [x] **Testing Infrastructure**
  - [x] Unit tests for interpreter (`tests/test_interpreter.py`)
  - [x] Unit tests for harvester (`tests/test_harvester.py`)
  - [x] End-to-end browser testing validation

### ✅ **Key Learnings from Previous Implementation**
- **Rate Limiting Issues**: OpenAI calls in interpreter + browser-use = frequent rate limits
- **Over-Engineering**: Structured parsing duplicates browser-use's natural language capabilities
- **Limited Flexibility**: Engagement type constraints prevent complex multi-step tasks
- **Architecture Insight**: browser-use is designed for direct natural language input

---

## **PHASE 1: ARCHITECTURE TRANSITION (TDD)**

**Objective:** Replace constrained interpreter with flexible prompt transformer while maintaining functionality.

### **1.1: PromptTransformer Implementation (TDD)**

- [ ] **Task 1.1.1: RED - Basic PromptTransformer Tests**
  - [ ] Create `tests/test_prompt_transformer.py`
  - [ ] Write failing test: `test_enhance_basic_prompt()`
    ```python
    def test_enhance_basic_prompt():
        transformer = PromptTransformer()
        user_prompt = "Like posts about AI"
        enhanced = transformer.enhance_prompt(user_prompt)
        assert "linkedin.com" in enhanced.lower()
        assert "ai" in enhanced.lower()
    ```
  - [ ] Write failing test: `test_validate_empty_prompt()`
  - [ ] Write failing test: `test_validate_malicious_prompt()`
  - [ ] **Verify**: All tests fail (RED confirmed)

- [ ] **Task 1.1.2: GREEN - Minimal PromptTransformer Implementation**
  - [ ] Create `prompt_transformer.py`
  - [ ] Implement minimal `PromptTransformer` class
    ```python
    class PromptTransformer:
        def enhance_prompt(self, user_prompt: str) -> str:
            # Minimal implementation to pass tests
    ```
  - [ ] Basic validation methods
  - [ ] **Verify**: All tests pass (GREEN confirmed)

- [ ] **Task 1.1.3: REFACTOR - Improve PromptTransformer**
  - [ ] Add LinkedIn context enhancement
  - [ ] Improve prompt optimization
  - [ ] Add safety validation
  - [ ] **Verify**: All tests still pass, code is cleaner

### **1.2: Harvester Simplification (TDD)**

- [ ] **Task 1.2.1: RED - String-Based Harvester Tests**
  - [ ] Update `tests/test_harvester.py`
  - [ ] Write failing test: `test_harvest_with_string_prompt()`
    ```python
    @patch('harvester.Agent')
    def test_harvest_with_string_prompt(self, mock_agent_class):
        harvester = Harvester()
        prompt = "Find 3 posts about renewable energy on LinkedIn"
        result = asyncio.run(harvester.harvest(prompt))
        # Assert Agent called with enhanced prompt
    ```
  - [ ] Remove all Command object tests
  - [ ] **Verify**: Tests fail due to signature mismatch (RED confirmed)

- [ ] **Task 1.2.2: GREEN - Update Harvester Signature**
  - [ ] Change `harvest(self, command: Command)` → `harvest(self, enhanced_prompt: str)`
  - [ ] Remove Command import and logic
  - [ ] Simplify task generation - direct prompt passing
  - [ ] **Verify**: Tests pass (GREEN confirmed)

- [ ] **Task 1.2.3: REFACTOR - Clean Up Harvester**
  - [ ] Remove engagement type branching
  - [ ] Improve error handling
  - [ ] Add prompt logging
  - [ ] **Verify**: Tests still pass, code is simpler

### **1.3: Flask App Migration (TDD)**

- [ ] **Task 1.3.1: RED - New Endpoint Tests**
  - [ ] Create `tests/test_app_integration.py`
  - [ ] Write failing test for simplified `/api/process` endpoint
  - [ ] Test PromptTransformer integration
  - [ ] **Verify**: Tests fail (RED confirmed)

- [ ] **Task 1.3.2: GREEN - Update Flask App**
  - [ ] Remove `from interpreter import PromptInterpreter, Command`
  - [ ] Add `from prompt_transformer import PromptTransformer`
  - [ ] Replace `/api/parse` and `/api/process_prompt_and_fetch` with single `/api/process`
  - [ ] Update flow: `prompt → transformer → harvester → response`
  - [ ] **Verify**: Tests pass, app runs (GREEN confirmed)

- [ ] **Task 1.3.3: REFACTOR - Simplify App Logic**
  - [ ] Clean up error handling
  - [ ] Improve response structure
  - [ ] Add request logging
  - [ ] **Verify**: Tests still pass, cleaner code

### **1.4: End-to-End Validation (TDD)**

- [ ] **Task 1.4.1: Manual E2E Testing**
  - [ ] Start Flask app: `venv/bin/python3 app.py`
  - [ ] Test simple prompt: "Show me posts about machine learning"
  - [ ] Test complex prompt: "Find AI researchers who graduated from Stanford and engage with their recent posts"
  - [ ] **Verify**: Both work without engagement type errors

- [ ] **Task 1.4.2: Automated E2E Tests**
  - [ ] Create `tests/test_e2e_transition.py`
  - [ ] Test full pipeline with mock browser-use
  - [ ] Compare functionality vs previous version
  - [ ] **Verify**: No regression in basic functionality

---

## **PHASE 2: ENHANCED CAPABILITIES & SAFETY (TDD)**

**Objective:** Add advanced prompt enhancement and safety features.

### **2.1: Advanced Prompt Enhancement (TDD)**

- [ ] **Task 2.1.1: RED - Complex Prompt Tests**
  - [ ] Test multi-step prompts: "Find CTOs at YC companies, check their recent posts about hiring, and comment thoughtfully"
  - [ ] Test profile management: "Update my headline to mention my new certification"
  - [ ] Test contextual understanding: "Look for people discussing the latest AI paper and engage"
  - [ ] **Verify**: Current implementation fails (RED confirmed)

- [ ] **Task 2.1.2: GREEN - Context-Aware Enhancement**
  - [ ] Add multi-step task breakdown in PromptTransformer
  - [ ] Add LinkedIn-specific context injection
  - [ ] Add persona integration for personalized responses
  - [ ] **Verify**: Complex prompts work (GREEN confirmed)

- [ ] **Task 2.1.3: REFACTOR - Optimize Enhancement Logic**
  - [ ] Improve prompt clarity for browser-use
  - [ ] Add task prioritization
  - [ ] Optimize for token efficiency
  - [ ] **Verify**: Same functionality, better performance

### **2.2: Safety & Validation (TDD)**

- [ ] **Task 2.2.1: RED - Safety Tests**
  - [ ] Test malicious prompt detection
  - [ ] Test spam prevention
  - [ ] Test professional boundary enforcement
  - [ ] **Verify**: Unsafe prompts currently pass through (RED confirmed)

- [ ] **Task 2.2.2: GREEN - Safety Implementation**
  - [ ] Add malicious intent detection
  - [ ] Add rate limiting guidance
  - [ ] Add professional conduct warnings
  - [ ] **Verify**: Safety tests pass (GREEN confirmed)

- [ ] **Task 2.2.3: REFACTOR - Improve Safety UX**
  - [ ] Add user education on safe prompts
  - [ ] Improve error messages
  - [ ] Add suggestion system for rejected prompts
  - [ ] **Verify**: Better user experience, same security

---

## **PHASE 3: TESTING & OPTIMIZATION (TDD)**

**Objective:** Comprehensive testing and performance optimization.

### **3.1: Performance Testing**

- [ ] **Task 3.1.1: Rate Limiting Mitigation**
  - [ ] Test token usage: new vs old system
  - [ ] Implement retry logic with exponential backoff
  - [ ] Add request queuing for high-volume usage
  - [ ] **Verify**: Reduced rate limiting incidents

- [ ] **Task 3.1.2: Response Time Optimization**
  - [ ] Profile prompt processing time
  - [ ] Optimize PromptTransformer logic
  - [ ] Add caching for common enhancements
  - [ ] **Verify**: Faster response times

### **3.2: Comprehensive Testing**

- [ ] **Task 3.2.1: Edge Case Coverage**
  - [ ] Test prompts in different languages
  - [ ] Test very long prompts
  - [ ] Test ambiguous prompts
  - [ ] Test error recovery scenarios
  - [ ] **Verify**: Robust handling of edge cases

- [ ] **Task 3.2.2: Integration Testing**
  - [ ] Test with actual LinkedIn (browser-use)
  - [ ] Test various browser states
  - [ ] Test network failure scenarios
  - [ ] **Verify**: Reliable real-world performance

---

## **PHASE 4: DOCUMENTATION & DEPLOYMENT (TDD)**

**Objective:** Document new capabilities and prepare for production.

### **4.1: Documentation Updates**

- [ ] **Task 4.1.1: Update README.md**
  - [ ] Document new natural language capabilities
  - [ ] Add example prompts (simple to complex)
  - [ ] Update setup instructions
  - [ ] Add troubleshooting guide

- [ ] **Task 4.1.2: Update Technical Documentation**
  - [ ] Update `SYSTEM_DESIGN.md` with new architecture
  - [ ] Document removed constraints
  - [ ] Add performance benchmarks
  - [ ] Update API documentation

### **4.2: User Guide & Examples**

- [ ] **Task 4.2.1: Create Prompt Examples Library**
  - [ ] Basic actions: "Like posts about X"
  - [ ] Advanced actions: "Find and engage with Y professionals"
  - [ ] Multi-step workflows: "Research topic X, then do Y"
  - [ ] Profile management: "Update my Z section"

- [ ] **Task 4.2.2: Best Practices Guide**
  - [ ] Effective prompt writing
  - [ ] Professional conduct guidelines
  - [ ] Rate limiting awareness
  - [ ] Safety considerations

### **4.3: Final Validation**

- [ ] **Task 4.3.1: Full System Test**
  - [ ] Test all documented examples
  - [ ] Validate performance improvements
  - [ ] Confirm no regressions
  - [ ] **Success Criteria**: All examples work, system is more capable than before

- [ ] **Task 4.3.2: Code Review & Cleanup**
  - [ ] Remove unused files/code
  - [ ] Update dependency list
  - [ ] Final lint and formatting
  - [ ] Update `CHANGELOG.md`

---

## **SUCCESS METRICS**

**Quantitative:**
- [ ] Lines of code reduced by >50%
- [ ] API calls reduced by >40%
- [ ] Rate limiting incidents reduced by >70%
- [ ] Response time improved by >30%

**Qualitative:**
- [ ] Support for complex multi-step tasks
- [ ] Natural language interface (no syntax learning)
- [ ] Enhanced LinkedIn capabilities
- [ ] Maintained safety and reliability

**Test Coverage:**
- [ ] >90% test coverage maintained
- [ ] All TDD cycles completed (RED-GREEN-REFACTOR)
- [ ] Zero regressions in core functionality
- [ ] Comprehensive edge case handling

---

## **ROLLBACK PLAN**

If critical issues arise during transition:
- [ ] **Phase 1 Rollback**: Revert to `interpreter.py` + `Command` objects
- [ ] **Phase 2 Rollback**: Disable advanced features, keep basic transformer
- [ ] **Full Rollback**: Git revert to pre-transition commit

**Rollback Triggers:**
- [ ] >50% increase in error rate
- [ ] Critical functionality completely broken
- [ ] Unresolvable security vulnerabilities
- [ ] Performance degradation >2x

---

This plan maintains our TDD discipline while transitioning to a more powerful, flexible architecture. Each phase builds incrementally with continuous validation of functionality.
