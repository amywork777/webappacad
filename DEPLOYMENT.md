# Deployment Guide

This guide covers how to deploy the AI-CAD Web Application to Render (backend) and Vercel (frontend).

## Prerequisites

Before deploying, ensure you have:

1. A GitHub account and repository with your code pushed
2. Render account (sign up at https://render.com)
3. Vercel account (sign up at https://vercel.com)
4. API keys for OpenAI and/or Anthropic

## Deploying the Backend to Render

The backend uses Docker to provide a consistent environment with FreeCAD and all necessary dependencies.

### Automatic Deployment

We've provided a script for automatic deployment:

```bash
./render-deploy.sh
```

This will:
1. Install render-cli if needed
2. Create a web service on Render
3. Configure environment variables
4. Start the deployment process

### Manual Deployment

#### Using Render Dashboard

1. Log in to your Render account
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Select "Docker" as the runtime
5. Configure the service:
   - Name: webcad-backend
   - Region: Your preferred region
   - Branch: main
   - Root Directory: / (leave empty)
   - Docker Command: uvicorn backend.main:app --host 0.0.0.0 --port 8080
   - Add Environment Variables:
     - OPENAI_API_KEY: your_openai_api_key
     - ANTHROPIC_API_KEY: your_anthropic_api_key
     - LLM_PROVIDER: openai (or anthropic)
6. Click "Create Web Service"

#### Using render.yaml (Infrastructure as Code)

1. Commit the `render.yaml` file to your repository
2. In Render dashboard, click "Blueprint" to create services from the YAML definition
3. Connect your GitHub repository
4. Render will detect the `render.yaml` file and create services accordingly
5. Add your API keys as environment variables through the Render dashboard

## Deploying the Frontend to Vercel

### Automatic Deployment

We've provided a script for automatic deployment:

```bash
./vercel-deploy.sh
```

This will:
1. Install Vercel CLI if needed
2. Link your local project to Vercel
3. Add the backend URL as an environment variable
4. Deploy to production

### Manual Deployment

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

3. Link to Vercel:
   ```bash
   vercel link
   ```

4. Add environment variables:
   ```bash
   vercel env add VITE_API_URL
   ```
   When prompted, enter the backend URL (e.g., https://webcad-backend.onrender.com)

5. Deploy to production:
   ```bash
   vercel --prod
   ```

### Vercel Dashboard Deployment

Alternatively, you can deploy directly from the Vercel dashboard:

1. Go to https://vercel.com and log in
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Configure project:
   - Framework Preset: Vite
   - Root Directory: ./frontend
   - Environment Variables:
     - VITE_API_URL: https://webcad-backend.onrender.com
5. Click "Deploy"

## Switching LLM Providers

To switch between OpenAI and Anthropic:

1. Log in to Render dashboard
2. Go to your webcad-backend service
3. Click on "Environment" tab
4. Change the `LLM_PROVIDER` value to either "openai" or "anthropic"
5. Click "Save Changes"
6. Trigger a manual deploy

This will restart your service with the new LLM provider.

## Testing the Deployment

After deployment is complete:

1. Visit your Vercel frontend URL (e.g., https://webappacad.vercel.app)
2. Try generating a 3D model from text:
   - Enter a text description like "cube with 50mm sides"
   - Click "Text → STEP"
   - You should get a download of the STEP file
3. Try generating a 3D model from an image:
   - Upload an image
   - You should get a download of the STEP file

## Troubleshooting

### Backend Issues

- Check Render logs for any errors
- Verify environment variables are set correctly
- Ensure the Docker build is completing successfully

### Frontend Issues

- Check Vercel deployment logs
- Verify the VITE_API_URL is pointing to your Render backend
- Check browser console for any errors
- Verify CORS is not blocking requests

### API Key Issues

- Ensure API keys are valid and have the necessary permissions
- Check for any rate limiting or billing issues with the LLM providers

If you encounter persistent issues, you may need to check the specific error messages in the Render or Vercel logs.