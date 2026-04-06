# CLAUDE.md

## Project Context

This is a music data management system for church music. The backend is a FastAPI JSON API following Clean Architecture. A React frontend is planned but not yet implemented.

## Current Tech Stack

- **Backend**: Python, FastAPI, PostgreSQL (asyncpg), SQLAlchemy 2.0 async, Alembic, PyJWT, httpx, pydantic-settings
- **Testing**: pytest, pytest-asyncio, aiosqlite (in-memory SQLite for tests)
- **Deployment**: Docker with Docker Compose, uvicorn

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

## Testing Standards

- **AAA Pattern**: All test implementations MUST strictly follow the **Arrange-Act-Assert** pattern. Visually separate these three phases within the test body using comments (`# Arrange`, `# Act`, `# Assert`) to maintain clear test structure.
- **BDD-Style Test Docstrings**: Every test function MUST include a docstring describing its exact behavior using the **Given-When-Then** format.

  _Example:_

  ```python
  def test_example_behavior():
      """
      GIVEN [precondition or initial state]
      WHEN [action or trigger]
      THEN [expected outcome or state change]
      """
      # Arrange
      ...

      # Act
      ...

      # Assert
      ...
  ```

## Code Quality & Documentation Principle

- **Type Hinting**: All arguments and return values in functions should be defined with strict types. No implicit types.
- **Production Code Docstrings**: MUST use **Google Style** docstrings for all classes, methods, and functions in the production code. Clearly document the `Args`, `Returns`, and `Raises` sections to define the API contract.
- **Linting & Formatting**: You MUST ALWAYS run the linter and formatter after changes to check the code quality. Use Ruff and Pyright as formatter and linter. Read `Project Commands` for more information if needed.
- **Clean Architecture**: Follow Clean Architecture principle by Robert C. Martin (Uncle Bob). Read `Clean Architecture Principle` for more information if needed.

## Check Documentation

- After complete each task or TODO, ALWAYS check and update the relevant documentations, readme, etc.
- Your document should be concise and hit the point, write down the critical note so that future maintainers can get started quickly.

## Key Documentation References

- **Project Commands**: `./docs/COMMANDS.md`
- **Clean Architecture Principle**: `./docs/CLEAN_ARCHITECTURE_PRINCIPLE.md`
- **Project Architecture**: `./docs/ARCHITECTURE.md`
- **Project Environment Variables**: `./docs/ENVIRONMENT_VARIABLES.md`
