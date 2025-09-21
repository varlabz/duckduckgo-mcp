# DuckDuckGo MCP / CLI

A Model Context Protocol (MCP) server and CLI that provide DuckDuckGo search functionality as MCP tools, resources, prompts, and a command-line interface.

## Features

- **Search Tool**: Structured web, images, videos, and news search with parameters
- **Prompts**: Pre-built prompts for search analysis and research planning
- **Resources**: Discover supported DuckDuckGo region codes
- **CLI**: Run searches from your terminal with JSON output option

## Use With MCP Clients

### Configure via uvx (Claude Desktop)

Add this to `~/Library/Application Support/Claude/claude_desktop_config.json` under `mcpServers`:

```json
{
  "mcpServers": {
    "duckduckgo": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/varlabz/duckduckgo-mcp",
        "duckduckgo-mcp"
      ]
    }
  }
}
```

Notes:
- Restart Claude Desktop after saving the config.

### Configure via uvx (VS Code)

Add this to your workspace `.vscode/mcp.json` (or User settings JSON):

```json
{
  "servers": {
    "duckduckgo": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/varlabz/duckduckgo-mcp",
        "duckduckgo-mcp"
      ]
    }
  }
}
```

### Quick sanity check (optional)

Run the server ad-hoc via uvx to verify it starts:

```bash
uvx --from git+https://github.com/varlabz/duckduckgo-mcp duckduckgo-mcp
```

### MCP Capabilities

- Tools: `search` — DuckDuckGo search across `text` (default), `images`, `videos`, or `news`.
  - Parameters:
    - `query` (string)
    - `max_results` (1–50, default 10)
    - `categories` (`text|images|videos|news`)
    - `region` (e.g., `us-en`; defaults to `us-en` when omitted)
    - `safesearch` (`on|moderate|off`, default `off`)
    - `timelimit` (`day|week|month|year`)
  - Returns: `query`, `total_results`, `results[{title, url, body}]`.
- Resources: `duckduckgo://regions` — JSON with `note`, `count`, and `regions[{code, name}]` to discover supported region codes.
- Prompts: `search_assistant(query, context="")` — generates a prompt to analyze search results; `research_planner(topic, depth="basic|intermediate|comprehensive")` — generates a structured research plan.

## Use as CLI Command

Run directly with uvx (no install):

```bash
uvx --from git+https://github.com/varlabz/duckduckgo-mcp duckduckgo-cli "python programming"
```

Or from this project (or after installing locally) using uv:

```bash
uv run duckduckgo-cli "python programming"
```

With options:

```bash
uv run duckduckgo-cli "python programming" \
  --max-results 20 \
  --region us-en \
  --safesearch on \
  --timelimit week \
  --categories text \
  --json
```

Available options:
- `--max-results`, `-m`: Maximum number of results (default: 10)
- `--region`, `-r`: Region code (e.g., `us-en`)
- `--safesearch`, `-s`: `on`, `moderate`, or `off` (default: `off`)
- `--timelimit`, `-t`: `day`, `week`, `month`, or `year`
- `--categories`, `-c`: `text` (default), `images`, `videos`, or `news`
- `--json`: Output results as JSON array
- `--resoure-regions`: Print the supported regions resource and exit
- `--prompt-search-assistant QUERY`: Print the `search_assistant` prompt text and exit
- `--prompt-search-assistant-context CTX`: Optional context for search assistant prompt
- `--prompt-research-planner TOPIC`: Print the `research_planner` prompt text and exit
- `--prompt-research-planner-depth DEPTH`: Depth for research planner (`basic`, `intermediate`, `comprehensive`)

Examples with uvx:

```bash
# JSON output for scripting
uvx --from git+https://github.com/varlabz/duckduckgo-mcp duckduckgo-cli \
  "api documentation" --json | jq .

# Generate a prompt for analyzing results
uvx --from git+https://github.com/varlabz/duckduckgo-mcp duckduckgo-cli \
  --prompt-search-assistant "best python web frameworks" \
  --prompt-search-assistant-context "target: 2025 stack, perf+ecosystem"

# List supported regions (human-readable)
uvx --from git+https://github.com/varlabz/duckduckgo-mcp duckduckgo-cli --resoure-regions

# List supported regions as JSON
uvx --from git+https://github.com/varlabz/duckduckgo-mcp duckduckgo-cli --resoure-regions --json

# Pin to a branch/tag/commit for reproducibility
uvx --from git+https://github.com/varlabz/duckduckgo-mcp@main duckduckgo-cli "golang tutorials"
```

## Development
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

## License

This project is licensed under the MIT License.