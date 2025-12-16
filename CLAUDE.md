# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Excalibur is a Python CLI tool that generates tuned prompts for AI coding assistants. It uses a knowledge base (KB) of prompt engineering techniques and the xAI Grok API to produce model-specific prompts optimized for tasks like debugging, planning, and execution.

## Development Commands

This project uses [mise](https://mise.jdx.dev/) for tool management. All commands below assume mise is installed.

```bash
# Lint
mise run lint           # Check with Ruff
mise run lint-fix       # Auto-fix lint issues

# Format
mise run format         # Format with Ruff
mise run format-check   # Check formatting

# Pre-commit hooks
mise run hooks-install  # Install prek + infisical hooks
mise run pre-commit-run # Run all hooks

# Run the CLI directly (UV inline script)
uv run src/excalibur/excalibur.py "your task" --model claude_code
```

## Architecture

The codebase is minimal by design. The main entry point is `src/excalibur/excalibur.py`, a UV inline script that:

1. Loads an embedded YAML knowledge base of prompt techniques (phases: planning, execution, debug)
2. Sends the KB + user task to Grok-4 via xAI SDK
3. Returns a tuned prompt for the specified model (claude_code, gemini_cli, chatgpt)

CLI flags: `--a-b` for A/B scoring, `--scrape` for KB patching, `--chain` for multi-turn refinement.

## Environment Setup

Required: `XAI_API_KEY` environment variable. Store in `mise.local.toml` (gitignored):

```toml
[env]
XAI_API_KEY = "your-key"
```

## Tooling

- Python 3.13, managed via mise
- UV for dependency resolution and script execution
- Ruff for linting/formatting
- prek for pre-commit hooks (with infisical for secrets scanning)
- git-cliff for changelog generation (conventional commits)

## Knowledge Base

The KB lives in `docs/kb/` as versioned YAML files. Each technique has:
- `technique`: Name
- `tip`: Usage guidance
- `model_tune`: Model-specific adaptations

Phases: planning, execution, debug. The embedded KB in `excalibur.py` should stay in sync with `docs/kb/v2.yaml`.
