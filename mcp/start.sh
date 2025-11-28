#!/bin/sh
docker build -t mcp-firebase-android .
docker run -p 8000:8000 mcp-firebase-android