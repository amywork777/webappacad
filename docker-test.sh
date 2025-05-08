#!/bin/bash

# This script tests the application using docker-compose
# It's an alternative to the test_commands.sh script

# Set up environment variables from .env file
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo "Error: .env file not found. Please create it from .env.example"
  exit 1
fi

# Start the application using docker-compose
echo "Starting the application with docker-compose..."
docker-compose up --build -d

# Wait for services to start
echo "Waiting for services to start..."
sleep 10

echo "Application is running!"
echo "- Backend API: http://localhost:8000"
echo "- Frontend UI: http://localhost:5173"

echo -e "\nPress Enter to stop the application and clean up..."
read

# Stop and remove containers
echo "Stopping the application..."
docker-compose down

echo "Test complete!"