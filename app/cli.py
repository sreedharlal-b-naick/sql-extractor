import typer
from app.flow import create_extract_flow
import os

app = typer.Typer()

DEFAULT_EXCLUDE_PATTERNS = [
    "venv/*", ".venv/*", "*test*", "tests/*", "docs/*", "examples/*", "v1/*",
    "dist/*", "build/*", "experimental/*", "deprecated/*",
    "legacy/*", ".git/*", ".github/*", ".next/*", ".vscode/*", "obj/*", "bin/*", "node_modules/*", "*.log"
]

@app.command()
def extract(
    repo_url: str = typer.Option(None, help="GitHub repository URL to extract queries from"),
    github_token: str = typer.Option(None, help="GitHub personal access token for accessing private repositories or avoiding rate limits"),
    local_dir: str = typer.Option("tests/data", help="Local directory to store repository files"),
    output_path: str = typer.Option("artifacts/queries.json", help="Path to save extracted queries"),
    include_patterns: list[str] = typer.Option(["*.sql", "*.erl"], help="File patterns to include"),
    exclude_patterns: list[str] = typer.Option(DEFAULT_EXCLUDE_PATTERNS, help="File patterns to exclude"),
    max_file_size: int = typer.Option(1000000, help="Maximum file size in bytes"),
    llm_provider: str = typer.Option("ollama", help="LLM provider to use (ollama, groq, or gemini)"),
):
    """Extract SQL queries from a GitHub repository or local directory."""

    shared = {
        "repo_url": repo_url,
        "local_dir": local_dir,
        "output_path": output_path,
        "include_patterns": include_patterns,
        "exclude_patterns": exclude_patterns,
        "max_file_size": max_file_size,
        "github_token": github_token,
        "llm_provider": llm_provider
    }

    extract_flow = create_extract_flow()
    extract_flow.run(shared)

if __name__ == "__main__":
    app()
