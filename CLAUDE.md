# CLAUDE.md

## Project Context

This is a music data management system for church music, based on Python Flask and PostgreSQL.
We are now going to refactor this project from a full-stack Flask project to a React and FastAPI project.

## Current Tech Stack

- **Backend**: Python, Flask, PostgreSQL, SQLAlchemy, Alembic, Docker with Docker Compose

## Development Principle

Use TDD development workflow. Strictly adhere to the Red-Green-Refactor TDD cycle. Writing or modifying implementation logic without a corresponding failing test is strictly prohibited.

### Workflow

#### 1. RED (Define Test)

- Write unit or integration tests based on requirements first.
- Must cover both the Happy Path and Edge Cases.
- Execute the test. The test MUST **Fail** to validate the test code's integrity.

#### 2. GREEN (Minimal Implementation)

- Write the **minimum necessary code** to pass the test.
- **No Test Overfitting**: Hardcoding return values to bypass test logic is strictly prohibited.
- Execute the test:
  - If Fail: Analyze the Error Trace, fix the implementation, and re-run.
  - If Pass: Proceed to Refactor.

#### 3. REFACTOR (Optimize)

- Improve code structure while ensuring "All tests remain passing."
- Enhance performance, remove technical debt, and eliminate duplicated code (DRY principle).
- Ensure compliance with Clean Code and Clean Architecture standards.
- Re-run tests after refactoring to confirm no breaking changes.

### Stopping Condition

The task is considered complete and ready to report ONLY when **All Tests Pass** and the code is fully refactored with no redundancy.

## Code Quality Principle

You MUST ALWAYS run the linter and formatter after changes to check the code quality.

Use Ruff and Pyright as formatter and linter. Read `Project Commands` for more information if needed.

Follow Clean Architecture principle by Robert C. Martin (Uncle Bob). Read `Clean Architecture Principle` for more information if needed.

## Key Documentation References

- **Project Commands**: `./docs/COMMANDS.md`
- **Clean Architecture Principle**: `./docs/CLEAN_ARCHITECTURE_PRINCIPLE.md`
- **Project Architecture**: `./docs/ARCHITECTURE.md`
- **Project Environment Variables**: `./docs/ENVIRONMENT_VARIABLES.md`
