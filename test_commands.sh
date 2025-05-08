#!/bin/bash

# This script contains the commands to test the application locally
# Note: This assumes Docker is running and the image has been built

# 1. Build Docker image (if not already built)
echo "Building Docker image..."
docker build -t webcad-fc .

# 2. Set up Python environment
echo "Setting up Python environment..."
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# 3. Set up environment variables (assuming .env file is configured)
export $(grep -v '^#' .env | xargs)

# 4. Start backend server
echo "Starting backend server..."
uvicorn backend.main:app --reload &
BACKEND_PID=$!

# 5. Start frontend development server
echo "Starting frontend..."
cd frontend
npm install
npm run dev &
FRONTEND_PID=$!

# Wait for servers to start
sleep 5

echo "Testing application..."
echo "Backend running at http://localhost:8000"
echo "Frontend running at http://localhost:5173"
echo ""
echo "You can now test the application by visiting http://localhost:5173 in your browser"
echo "To test text-to-CAD: Enter a text description and click 'Text → STEP'"
echo "To test image-to-CAD: Choose an image file using the file input"
echo ""
echo "Press Ctrl+C to stop the servers when done"

# Wait for user to press Ctrl+C
wait $BACKEND_PID $FRONTEND_PID

# Cleanup
deactivate