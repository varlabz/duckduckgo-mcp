# DuckDuckGo Python Project - Copilot Instructions

## Project Overview
This is a Python project called "duckduckgo" that provides functionality related to DuckDuckGo services. The project is structured as a modern Python package with comprehensive tooling for development, testing, and code quality.

## Technology Stack
- **Python Version**: 3.12+
- **Build System**: setuptools
- **Dependency Management**: uv
- **Linting & Formatting**: Ruff
- **Testing**: pytest
- **Version Control**: Git

## Project Structure
```
├── pyproject.toml          # Project configuration and dependencies
├── src/duckduckgo/         # Main package source code
│   └── __init__.py
├── tests/                  # Test files
│   └── test_*.py
└── README.md              # Project documentation
```

## Development Practices

### Environment Setup
- Use `uv venv` to create virtual environment
- Activate with `source .venv/bin/activate`
- Install dependencies with `uv sync`
- Add dependencies with `uv add` or `uv add --dev` for development tools

### Code Quality
- **Linting**: Run `uv run ruff check` to check code quality
- **Formatting**: Run `uv run ruff format` to format code
- **Rules**: Extensive Ruff configuration covering style, imports, complexity, and best practices
- **Ignored Rules**: S101 (assert statements), COM812 (trailing comma), ISC001 (import sorting conflicts)

### Testing
- **Framework**: pytest
- **Test Location**: `tests/` directory
- **Naming Convention**: `test_*.py` files, `Test*` classes, `test_*` functions
- **Running Tests**: `uv run pytest`

### Building
- **Build Command**: `uv build`
- **Distribution**: Wheel and source distribution

## Coding Standards

### Python Version Compatibility
- Target Python 3.12+
- Use modern Python features and syntax
- Follow PEP 8 style guidelines (enforced by Ruff)

### Import Organization
- Use absolute imports within the package
- Group imports: standard library, third-party, local
- Ruff handles import sorting automatically

### Error Handling
- Use appropriate exception types
- Provide meaningful error messages
- Handle edge cases gracefully

### Documentation
- Add docstrings to public functions and classes
- Keep comments clear and concise
- Update documentation when changing functionality

## Common Patterns

### Package Structure
- Keep business logic in `src/duckduckgo/`
- Use `__init__.py` for package initialization
- Export public API through `__init__.py`

### Testing
- Write unit tests for all public functions
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies when needed

### Dependency Management
- Add runtime dependencies to `pyproject.toml` under `[project.dependencies]`
- Add development tools to `[project.optional-dependencies.dev]`
- Use `uv add` to manage dependencies
- Pin versions for reproducibility

## Best Practices

### Commit Messages
- Use clear, descriptive commit messages
- Follow conventional commit format when possible
- Reference issue numbers when applicable

### Code Reviews
- Ensure all tests pass before submitting
- Run linting and formatting checks
- Verify documentation is updated
- Test edge cases and error conditions

### Performance
- Write efficient algorithms
- Avoid unnecessary computations
- Use appropriate data structures
- Profile code when performance is critical

## Getting Help
- Check the README.md for setup instructions
- Review pyproject.toml for project configuration
- Look at existing tests for examples
- Run `uv run ruff check --help` for linting options
