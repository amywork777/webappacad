#!/bin/bash

# Activate the virtual environment if it exists
if [ -d "venv" ]; then
  source venv/bin/activate
fi

# Set the test mode environment variable
export TEST_MODE=true

# Start the backend server
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Deactivate virtual environment when done
deactivate 