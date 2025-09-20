# DuckDuckGo

A Python project.

## Setup

### Virtual Environment

Create a virtual environment using uv:

```bash
uv venv
```

Activate it:

```bash
source .venv/bin/activate
```

### Dependencies

Install dependencies:

```bash
uv sync
```

Add new dependencies:

```bash
uv add package_name
```

For development dependencies:

```bash
uv add --dev package_name
```

### Linting

Run linting with ruff:

```bash
uv run ruff check
```

Format code:

```bash
uv run ruff format
```

### Testing

Run tests with pytest:

```bash
uv run pytest
```

### Building

Build the project:

```bash
uv build
```

## Version Control

This project uses Git for version control.

Initialize repository:

```bash
git init
```

Add files:

```bash
git add .
```

Commit:

```bash
git commit -m "Initial commit"
```