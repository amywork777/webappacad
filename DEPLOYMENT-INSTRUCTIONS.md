# AI-CAD Web Application Deployment Instructions

## 1. Local Testing (WITHOUT Docker)

If you want to test the application without setting up Docker:

### Step 1: Set Up Environment

```sh
# Activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install backend dependencies
pip install -r backend/requirements.txt
```

### Step 2: Start Test Backend

```sh
# This uses a test mode that doesn't require Docker
./run_test_backend.sh
```

The backend will run in test mode, simulating FreeCAD operations without actually running them.

### Step 3: Start Frontend

In a separate terminal:

```sh
./run_test_frontend.sh
```

Visit http://localhost:5173 to use the application.

## 2. Prerequisites for Production Deployment

Before proceeding with deployment, ensure you have:

- Your code is pushed to GitHub at: https://github.com/amywork777/webappacad
- API keys for OpenAI and/or Anthropic
- Render and Vercel accounts

## 3. Backend Deployment (Render)

### Step 1: Set Environment Variables

```sh
# Replace with your actual API keys
export OPENAI_API_KEY=your_openai_key_here
export ANTHROPIC_API_KEY=your_anthropic_key_here
export LLM_PROVIDER=openai  # or anthropic
```

### Step 2: Run Render Deployment Script

```sh
./render-deploy.sh
```

This will:
- Create a new web service on Render
- Set up Docker environment
- Configure environment variables
- Start the deployment process

### Step 3: Monitor Deployment

Check the Render dashboard for deployment status. It may take several minutes to complete.

The backend URL will typically be: `https://webcad-backend.onrender.com`

## 4. Frontend Deployment (Vercel)

### Step 1: Run Vercel Deployment Script

```sh
./vercel-deploy.sh
```

When prompted, enter the backend URL (e.g., `https://webcad-backend.onrender.com`).

This will:
- Link your project to Vercel
- Set up environment variables
- Deploy the frontend

### Step 2: Monitor Deployment

Check the Vercel dashboard for deployment status.
The frontend URL will be displayed in the command output or available in your Vercel dashboard.

## 5. Testing the Deployment

1. Visit your frontend URL
2. Try a text prompt: "cube with 50mm sides"
3. Click "Text → STEP" to generate a model
4. Upload an image to test image-to-CAD functionality

## 6. Troubleshooting

If you encounter issues:

1. Check Render logs for backend errors
2. Check Vercel logs for frontend errors
3. Verify API keys are valid and properly set
4. Ensure the backend URL is correctly configured in the frontend

For detailed troubleshooting, refer to the DEPLOYMENT.md file. 