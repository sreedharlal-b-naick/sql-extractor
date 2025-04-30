# SQL Query Extractor

A Python tool for extracting SQL queries from code repositories, supporting both local directories and GitHub repositories. Available as both a command-line tool and a web interface.

## Features

- Extract SQL queries from code files
- Support for both local directories and GitHub repositories
- Configurable file patterns for inclusion/exclusion
- JSON output format
- GitHub integration with personal access token support
- File size limits for processing
- Web interface using Streamlit for easy interaction
- Multiple LLM provider support (Ollama, Groq, Gemini)

## Installation

The project uses Poetry for dependency management. To install:

```bash
# Clone the repository
git clone https://github.com/sreedharlal-b-naick/sql-extractor
cd sql-extractor

# Install dependencies
poetry install
```

## LLM Provider Setup

### Ollama (Default)

1. Install Ollama from: https://ollama.com/download
2. Pull the required model:
   ```bash
   ollama pull llama3.1:latest
   ```

### Groq

1. Get your API key from [Groq Console](https://console.groq.com/)
2. Add to `.env` file:
   ```
   GROQ_API_KEY=your-api-key-here
   ```

### Gemini

1. Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Add to `.env` file:
   ```
   GEMINI_API_KEY=your-api-key-here
   ```

## Usage

### Web Interface

The easiest way to use the tool is through the web interface:

```bash
# Start the Streamlit web interface
poetry run web
```

The web interface provides:
- Easy configuration of source (GitHub or local)
- Visual file pattern selection
- Real-time extraction status
- Interactive query viewing
- JSON download capability
- LLM provider selection and configuration

### Command Line Interface

For scriptable usage, you can use the CLI:

```bash
# Extract queries from a local directory using Ollama (default)
poetry run cli --local-dir /path/to/code

# Extract queries from a GitHub repository using Groq
poetry run cli --repo-url https://github.com/username/repo --llm-provider groq

# Extract queries from a GitHub repository using Gemini
poetry run cli --repo-url https://github.com/username/repo --llm-provider gemini
```

### Advanced Options

```bash
# Extract queries with custom patterns and output path
poetry run cli \
    --repo-url https://github.com/username/repo \
    --include-patterns "*.sql" "*.erl" \
    --output-path queries.json \
    --max-file-size 1000000 \
    --llm-provider groq
```

### Command Line Options

- `--repo-url`: GitHub repository URL (optional)
- `--github-token`: GitHub personal access token (optional)
- `--local-dir`: Local directory path (default: "tests/data")
- `--output-path`: Output file path (default: "queries.json")
- `--include-patterns`: File patterns to include (default: ["*.sql", "*.erl"])
- `--exclude-patterns`: File patterns to exclude
- `--max-file-size`: Maximum file size in bytes (default: 1000000)
- `--llm-provider`: LLM provider to use (default: "ollama")

## Development

### Setup

1. Install Poetry if you haven't already
2. Clone the repository
3. Run `poetry install` to install dependencies
4. Run `poetry shell` to activate the virtual environment

### Testing

```bash
poetry run pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
