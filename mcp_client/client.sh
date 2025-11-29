#!/bin/sh

# Docker build and run commands
docker build -t mcp-firebase-android-client .
# Run MCP client
docker run -p 9000:9000 mcp-firebase-android-client