# System Design

This document outlines the system design for the LinkedIn AI Agent, based on the requirements specification.

## 5.1 High-Level Diagram

The agent follows a sequential pipeline architecture:

```
Prompt  →  Prompt Interpreter  →  Command JSON
                     ↓
             Feed Harvester (Browser Use)
                     ↓
               Filter Engine
                     ↓
           Research & Comment Generator
                     ↓
         ┌────────────┴────────────┐
         │                         │
   Supervised UI             Autonomous
         │                         │
     User Choice             Engagement Executor
         └────────────┬────────────┘
                      ↓
                Logging Layer
```

## 5.2 Key Classes / Modules

| Module             | Core Classes / Functions                                    |
| :----------------- | :---------------------------------------------------------- |
| `interpreter.py`   | `def parse_prompt(raw:str)->Command`                        |
| `harvester.py`     | `class FeedScraper (methods: scroll(), extract_posts())`    |
| `filter_engine.py` | `apply_filters(posts, rules)`                               |
| `researcher.py`    | `enrich_post(post)->ResearchBundle`                         |
| `commenter.py`     | `draft_comment(bundle)->str`                                |
| `executor.py`      | `Engager.like(), .comment(), .message()`                    |
| `logger.py`        | `Logger.write(action_dict)`                                 |
| `config/`          | `settings.yaml`, `persona.md`, `filters.yaml`               |
