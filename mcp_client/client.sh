#!/bin/sh

# Docker build and run commands
docker build -t mcp-firebase-android-client .
# Run MCP client
docker run mcp-firebase-android-client