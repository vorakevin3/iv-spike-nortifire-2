#!/bin/bash
echo "Starting IV Spike Notifier..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
