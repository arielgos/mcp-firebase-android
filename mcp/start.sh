#!/bin/sh
docker build -t mcp-firebase-android .
docker run -p 8080:8080 mcp-firebase-android