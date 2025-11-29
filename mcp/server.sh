#!/bin/sh

# Docker build and run commands
docker build -t mcp-firebase-android .
# Run MCP server
docker run -p 8000:8000 mcp-firebase-android
# ngrok http 8000