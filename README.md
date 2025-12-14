mcp-fastmcp-starter

A minimal, production-minded MCP-shaped tool server scaffold for building agentic AI services with typed tool contracts, explicit invocation semantics, and deterministic JSON I/O, served via FastAPI.

This repository is intentionally small, explicit, and boring in the right ways. It is designed to demonstrate how an agent-facing service should be shaped, not to hide behavior behind abstractions.

What this is

This project provides a runnable starter for exposing tools to agent runtimes in an MCP-style pattern:

Explicit tool registry

Machine-readable input schemas

Typed request/response contracts

Deterministic invocation surface

Clean lifecycle and error handling

Testable and CI-verified

It is meant to be cloned, understood in minutes, and extended safely.



Architecture at a glance

The server exposes three core HTTP surfaces:

Client / Agent Runtime
        |
        |  GET  /tools        → discover available tools + schemas
        |  POST /invoke       → invoke tool with typed JSON args
        |  GET  /healthz      → liveness check
        |
FastAPI Runtime
        |
Typed validation (Pydantic)
        |
Tool execution
        |
Structured JSON result or error


|||

This mirrors how MCP-style systems expect to reason about tools: discoverable, schema-driven, and explicitly invoked.

Tool model

Tools are defined with:

A stable name

A human-readable description

A machine-readable input schema

A strictly typed output shape

At runtime, all inputs are validated and all outputs are JSON-serializable.

Example tools included:

sayHello – returns a greeting with a timestamp

reverse – reverses input text and returns metadata

These are trivial by design; the shape is the point.

Run locally

Create and activate a virtual environment:

python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"

Start the server:

./scripts/run_local.sh

Try it

Health check:

curl http://127.0.0.1:8000/healthz

List available tools (schemas included):

curl http://127.0.0.1:8000/tools | python -m json.tool

Invoke a tool:

curl http://127.0.0.1:8000/invoke \
  -H 'content-type: application/json' \
  -d '{
    "tool": "sayHello",
    "args": { "name": "Dennis" },
    "trace_id": "demo-1"
  }' | python -m json.tool


Testing

Tests are first-class and run locally and in CI.

python -m pytest -q


The test suite verifies:

Tool discovery

Input validation

Successful invocation

Error behavior for unknown tools

CI

This repository includes a GitHub Actions workflow that runs on every push and pull request:

Dependency install

Linting with Ruff

Full test suite via pytest

A green check here means the service is runnable in a clean environment.







