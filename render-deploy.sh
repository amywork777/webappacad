#!/bin/bash

# Script to deploy the backend to Render

# Check if render-cli is installed
if ! command -v render &> /dev/null; then
    echo "render-cli not found, installing..."
    npm i -g render-cli
fi

# Deploy to Render
echo "Deploying backend to Render..."
render services create web --name webcad-backend \
  --env Docker --branch main --repo https://github.com/amywork777/webappacad \
  --envVars OPENAI_API_KEY=$OPENAI_API_KEY,ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY,LLM_PROVIDER=$LLM_PROVIDER \
  --startCommand "uvicorn backend.main:app --host 0.0.0.0 --port 8080" \
  --port 8080

echo "Backend deployment initiated. It may take a few minutes to complete."
echo "Check the Render dashboard for deployment status."