#!/usr/bin/env bash
set -euo pipefail
uvicorn mcp_fastmcp_starter.server:app --host 127.0.0.1 --port 8000 --reload
