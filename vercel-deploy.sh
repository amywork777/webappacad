#!/bin/bash

# Script to deploy the frontend to Vercel

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "Vercel CLI not found, installing..."
    npm i -g vercel
fi

# Get the backend URL
read -p "Enter the backend URL (default: https://webcad-backend.onrender.com): " BACKEND_URL
BACKEND_URL=${BACKEND_URL:-https://webcad-backend.onrender.com}

# Update vercel.json with the correct backend URL
sed -i "s|https://webcad-backend.onrender.com|${BACKEND_URL}|g" frontend/vercel.json

# Deploy to Vercel
echo "Deploying frontend to Vercel..."
cd frontend
vercel link --yes
vercel env add VITE_API_URL production "${BACKEND_URL}" --yes
vercel --prod

echo "Frontend deployment initiated."
echo "Check the Vercel dashboard for deployment status."