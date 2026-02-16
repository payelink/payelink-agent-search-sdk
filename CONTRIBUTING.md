# Contributing to Payelink Agent Search SDK

Thank you for your interest in contributing to **Payelink Agent
Search**.

This project implements the Payelink Agent Discovery Protocol and aims
to provide a stable, secure, and well-documented reference SDK for
registry-based AI agent discovery.

We welcome contributions that improve:

-   Protocol clarity
-   SDK stability
-   Documentation quality
-   Performance
-   Security
-   Developer experience

------------------------------------------------------------------------

## Table of Contents

-   Ways to Contribute
-   Development Setup
-   Branching Strategy
-   Pull Request Guidelines
-   Coding Standards
-   Documentation Guidelines
-   Testing Requirements
-   Spec Changes
-   Reporting Issues
-   Code of Conduct

------------------------------------------------------------------------

## Ways to Contribute

You can contribute in several ways:

### 1. Bug Reports

Report issues with clear reproduction steps.

### 2. Feature Requests

Suggest improvements to: - Agent discovery - Filtering logic - Registry
validation - Error handling - Async performance

### 3. Documentation Improvements

Clarify examples, fix typos, improve structure, or expand explanations.

### 4. Protocol & Spec Enhancements

Propose improvements to: - `/.well-known/agents.json` - Agent
Card schema - Identity integration - Security model

------------------------------------------------------------------------

## Development Setup

### 1. Fork the Repository

Fork the repository to your GitHub account.

### 2. Clone Your Fork

```bash
git clone https://github.com/<your-username>/payelink-agent-search-sdk.git
cd payelink-agent-search-sdk
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
# or: venv\Scripts\activate  # Windows
```

### 4. Install Dependencies

The project uses `pyproject.toml`. Install in editable mode with dev dependencies:

```bash
pip install -e ".[dev]"
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv sync --all-extras
```

------------------------------------------------------------------------

## Branching Strategy

-   `main` → Stable branch
-   `feature/<short-description>`
-   `fix/<short-description>`
-   `docs/<short-description>`

Example:

git checkout -b feature/add-registry-signature-validation

------------------------------------------------------------------------

## Pull Request Guidelines

Before submitting a PR:

-   Ensure code passes tests
-   Add tests for new functionality
-   Update documentation if behavior changes
-   Keep PRs focused and minimal
-   Write a clear PR description

PR description should include:

-   What changed
-   Why it changed
-   Any breaking changes
-   Migration notes (if applicable)

------------------------------------------------------------------------

## Coding Standards

### Python Style

-   Follow PEP 8
-   Use type hints consistently
-   Prefer explicit over implicit behavior
-   Avoid global state
-   Keep functions small and focused

### Naming Conventions

-   Classes: PascalCase
-   Functions: snake_case
-   Constants: UPPER_CASE
-   Internal/private helpers: \_prefix_with_underscore

### Error Handling

-   Raise specific SDK errors
-   Avoid silent failures
-   Provide clear error messages

------------------------------------------------------------------------

## Documentation Guidelines

-   Use clear, direct language
-   Prefer active voice
-   Address the reader as "you"
-   Include code examples
-   Keep terminology consistent
-   Avoid marketing language

All protocol changes must update:

-   README
-   Specification (see README § Agent Registry Specification and `examples/agents.json`)
-   Example registry: `examples/agents.json`

------------------------------------------------------------------------

## Testing Requirements

All new features must include tests.

Run tests with:

```bash
pytest
```

Run the linter (PEP 8):

```bash
ruff check .
```

Testing principles:

-   Test success paths
-   Test failure paths
-   Test malformed registries
-   Test network failures
-   Test async and sync parity

------------------------------------------------------------------------

## Spec Changes

Changes to the Payelink Discovery Protocol must:

1.  Propose a version increment (e.g., v0.2)
2.  Document backward compatibility
3.  Provide migration guidance
4.  Update schema examples

Spec changes should be discussed in an issue before implementation.

------------------------------------------------------------------------

## Reporting Issues

When reporting an issue, include:

-   Python version
-   SDK version
-   Operating system
-   Steps to reproduce
-   Expected behavior
-   Actual behavior

Use clear titles like:

-   Async search hangs on invalid registry
-   Capability filter ignores defaultInputModes

------------------------------------------------------------------------

## Code of Conduct

We are committed to fostering an open and respectful community.

By participating, you agree to:

-   Be respectful and constructive
-   Provide helpful feedback
-   Avoid harassment or discriminatory behavior

Project maintainers reserve the right to remove contributions that do
not align with these principles.

------------------------------------------------------------------------

## Philosophy

Payelink Agent Search is infrastructure software.

We prioritize:

-   Clarity over cleverness
-   Stability over rapid feature growth
-   Explicit standards over hidden behavior
-   Security over convenience

Thank you for contributing to interoperable AI agent infrastructure.
