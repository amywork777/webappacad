#!/bin/bash

# Master deployment script for both backend and frontend

echo "AI-CAD Web Application Deployment"
echo "================================="
echo ""
echo "This script will deploy both the backend to Render and frontend to Vercel."
echo ""

# Check for API keys
if [ -z "$OPENAI_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "Warning: Neither OPENAI_API_KEY nor ANTHROPIC_API_KEY environment variables are set."
  echo "At least one API key is required for the application to function."
  
  read -p "Do you want to continue anyway? (y/n): " continue_deployment
  if [ "$continue_deployment" != "y" ]; then
    echo "Deployment cancelled."
    exit 1
  fi
fi

# Set default LLM provider if not specified
if [ -z "$LLM_PROVIDER" ]; then
  if [ -n "$OPENAI_API_KEY" ]; then
    export LLM_PROVIDER=openai
  elif [ -n "$ANTHROPIC_API_KEY" ]; then
    export LLM_PROVIDER=anthropic
  else
    # Default fallback
    export LLM_PROVIDER=openai
  fi
  echo "Using LLM_PROVIDER=$LLM_PROVIDER"
fi

# Deploy backend
echo ""
echo "Deploying backend to Render..."
./render-deploy.sh

# Get backend URL
echo ""
echo "Once the backend is deployed, you'll need its URL."
read -p "Enter the backend URL (default: https://webcad-backend.onrender.com): " BACKEND_URL
BACKEND_URL=${BACKEND_URL:-https://webcad-backend.onrender.com}

# Deploy frontend
echo ""
echo "Deploying frontend to Vercel..."
BACKEND_URL=$BACKEND_URL ./vercel-deploy.sh

echo ""
echo "Deployment process complete!"
echo "Backend: $BACKEND_URL"
echo "Frontend: Check the Vercel CLI output for the frontend URL"