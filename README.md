# DuckDuckGo MCP Server

A Model Context Protocol (MCP) server that provides DuckDuckGo search functionality as MCP tools, resources, and prompts.

## Requirements

- **Python**: 3.12 or higher
- **Dependencies**: 
  - `ddgs>=9.6.0` - DuckDuckGo search API client
  - `mcp[cli]>=1.14.0` - Model Context Protocol server framework

## Features

- **Web Search Tool**: Perform structured web searches with customizable parameters
- **Quick Search Tool**: Simple text-based search results for quick lookups
- **Search Resources**: Access recent search results via MCP resources
- **Search Prompts**: Pre-built prompts for search analysis and research planning

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

## Usage

### Development Mode

Run the MCP server in development mode with the MCP Inspector:

```bash
uv run mcp dev src/duckduckgo/mcp.py
```

### Install in Claude Desktop

Install the server in Claude Desktop:

```bash
uv run mcp install src/duckduckgo/mcp.py
```

Or with a custom name:

```bash
uv run mcp install src/duckduckgo/mcp.py --name "DuckDuckGo Search"
```

### Direct Execution

Run the server directly:

```bash
uv run python src/duckduckgo/mcp.py
```

## Available Tools

### `search`
Perform a structured web search using DuckDuckGo.

**Parameters:**
- `query` (string): The search query
- `max_results` (integer, 1-50): Maximum number of results to return (default: 10)
- `region` (string, optional): Region code (e.g., 'us-en', 'uk-en', 'de-de')
- `safesearch` (string): Safe search level - 'on', 'moderate', 'off' (default: 'off')
- `timelimit` (string, optional): Time limit - 'day', 'week', 'month', 'year'

**Returns:** Structured search results with titles, URLs, and body snippets.

## Available Resources

### `search://recent/{query}`
Get recent search results for a query as a resource.

Example: `search://recent/python programming`

## Available Prompts

### `search_assistant`
Generate a prompt for analyzing search results.

**Parameters:**
- `query` (string): The search query
- `context` (string, optional): Additional context for the analysis

### `research_planner`
Generate a structured research planning prompt.

**Parameters:**
- `topic` (string): The research topic
- `depth` (string): Research depth - 'basic', 'intermediate', 'comprehensive' (default: 'basic')

## CLI Usage

The project includes two command-line interfaces:

### DuckDuckGo Search CLI

Search directly from the command line:

```bash
uv run duckduckgo "python programming"
```

With options:

```bash
uv run duckduckgo "python programming" --max-results 20 --region us-en --safesearch on
```

Available options:
- `--max-results`, `-m`: Maximum number of results (default: 10)
- `--region`, `-r`: Region code (e.g., us-en)
- `--safesearch`, `-s`: Safe search level ('on', 'moderate', 'off', default: 'off')
- `--timelimit`, `-t`: Time limit ('d', 'w', 'm', 'y' for day, week, month, year)
- `--json`: Output results as JSON array

### MCP Server CLI

Run the MCP server directly:

```bash
uv run duckduckgo-mcp
```

## API Reference

### Python API

You can also use DuckDuckGo search programmatically in your Python code:

```python
from duckduckgo import search

# Basic search
results = search("python programming")

# Advanced search with parameters
results = search(
    "python programming",
    max_results=20,
    region="us-en",
    safesearch="moderate",
    timelimit="w"  # past week
)

# Each result contains:
# - title: The page title
# - href: The URL
# - body: The search result snippet
```

**Parameters:**
- `query` (str): The search query
- `max_results` (int): Maximum number of results (default: 10)
- `region` (str, optional): Region code (e.g., 'us-en', 'uk-en', 'de-de')
- `safesearch` (str): Safe search level - 'on', 'moderate', 'off' (default: 'off')
- `timelimit` (str, optional): Time limit - 'd', 'w', 'm', 'y' (day, week, month, year)

## Examples

### Basic Search

```bash
# Simple web search
uv run duckduckgo "machine learning"

# Search with more results
uv run duckduckgo "python tutorials" --max-results 20
```

### Advanced Search

```bash
# Search with region and safe search
uv run duckduckgo "news" --region us-en --safesearch moderate

# Search recent results only
uv run duckduckgo "technology trends" --timelimit w

# Get JSON output for scripting
uv run duckduckgo "api documentation" --json > results.json
```

### MCP Server Usage

```bash
# Development mode
uv run mcp dev src/duckduckgo/mcp.py

# Install in Claude Desktop
uv run mcp install src/duckduckgo/mcp.py --name "DuckDuckGo Search"
```

### Python Integration

```python
from duckduckgo import search

# Search and process results
results = search("artificial intelligence", max_results=15)
for result in results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['href']}")
    print(f"Snippet: {result['body'][:100]}...")
    print("---")
```

## Troubleshooting

### Common Issues

**No results returned**
- Check your internet connection
- Try a different search query
- Verify the region parameter is valid

**MCP server won't start**
- Ensure all dependencies are installed: `uv sync`
- Check that Python 3.12+ is being used
- Verify the MCP CLI tools are available

**CLI command not found**
- Make sure you're in the project directory
- Try running with `uv run` prefix
- Check that the virtual environment is activated

### Getting Help

- Check the [MCP documentation](https://modelcontextprotocol.io/) for server setup
- Review the [ddgs library documentation](https://github.com/deedy5/ddgs) for search parameters
- Open an issue on the project repository for bugs or feature requests

## Contributing

We welcome contributions! Here's how you can help:

### Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/duckduckgo-mcp.git`
3. Set up the development environment:
   ```bash
   cd duckduckgo-mcp
   uv venv
   source .venv/bin/activate
   uv sync
   ```

### Code Quality

- **Linting**: `uv run ruff check`
- **Formatting**: `uv run ruff format`
- **Testing**: `uv run pytest`
- **Type checking**: Ensure all code follows Python type hints

### Submitting Changes

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes and ensure tests pass
3. Run linting and formatting
4. Submit a pull request with a clear description

### Guidelines

- Follow PEP 8 style guidelines
- Add tests for new functionality
- Update documentation for API changes
- Keep commits focused and descriptive
- Ensure backward compatibility when possible

## Development

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

## License

This project is licensed under the MIT License.