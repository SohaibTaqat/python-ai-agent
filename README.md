# AI Agent

A simple command-line AI coding agent built with Google's Gemini API. Give it a
prompt and it will plan and execute function calls to inspect and modify files
within a sandboxed working directory.

## Capabilities

The agent can:

- List files and directories
- Read file contents
- Execute Python files (with optional arguments)
- Write or overwrite files

All file operations are constrained to the working directory for safety.

## Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

1. Install dependencies:

   ```bash
   uv sync
   ```

2. Create a `.env` file in the project root with your Gemini API key:

   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

```bash
uv run main.py "your prompt here"
```

Enable verbose output (token counts and function call results) with `--verbose`:

```bash
uv run main.py "your prompt here" --verbose
```

### Example

```bash
uv run main.py "Explain how the calculator renders the result to the console."
```

## How it works

`main.py` runs a loop (up to 20 iterations) that:

1. Sends the conversation to the Gemini model along with the available tools.
2. Executes any function calls the model requests via `call_function`.
3. Feeds the results back into the conversation.
4. Prints the final text response once the model stops calling functions.

If the iteration limit is reached without a final response, the program exits
with a non-zero status.

## Project layout

| Path                | Purpose                                          |
| ------------------- | ------------------------------------------------ |
| `main.py`           | Entry point and agent loop                       |
| `prompt.py`         | System prompt                                    |
| `call_function.py`  | Function-call dispatch and tool declarations     |
| `config.py`         | Configuration (e.g. max file read size)          |
| `functions/`        | Tool implementations (list, read, run, write)    |
| `calculator/`       | Example project the agent operates on            |
| `test_*.py`         | Tests for the tool functions                     |
