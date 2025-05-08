# AI-CAD Web Application

This is a web application that connects AI models (OpenAI or Anthropic) to CAD (Computer-Aided Design) functionality using FreeCAD.

## Features

- Text-to-CAD: Generate 3D models from text descriptions using LLMs
- Image-to-CAD: Convert images to 3D models using MCP (Machine learning for CAD Parameters)
- Technical Drawing: Generate PDF technical drawings from 3D models
- Finite Element Analysis (FEA): Run structural analysis on 3D models

## Project Structure

```
webappacad/
├── Dockerfile
├── backend/
│   ├── main.py            - FastAPI server
│   ├── llm.py             - Dual LLM provider support (OpenAI/Anthropic)
│   ├── utils.py           - Docker execution helpers
│   ├── fem_script.py      - Finite Element Analysis script
│   └── requirements.txt   - Python dependencies
├── frontend/
│   ├── vite.config.js     - Vite configuration
│   └── src/App.jsx        - React UI
└── .env.example           - Environment variables template
```

## Local Setup

### Prerequisites

- Docker
- Python 3.x
- Node.js

### Backend Setup

```bash
# Build Docker image
docker build -t webcad-fc .

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r backend/requirements.txt

# Configure environment variables (copy .env.example to .env and fill in API keys)
cp .env.example .env
# Edit .env with your API keys

# Run backend
uvicorn backend.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:5173 to use the application.

## Deployment

### Backend (Render)

```bash
npm i -g render-cli
render services create web --name webcad-backend \
  --env Docker --branch main --repo https://github.com/yourusername/webappacad \
  --envVars OPENAI_API_KEY=$OPENAI_API_KEY,ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY,LLM_PROVIDER=$LLM_PROVIDER \
  --startCommand "uvicorn backend.main:app --host 0.0.0.0 --port 8080" \
  --port 8080
```

### Frontend (Vercel)

```bash
npm i -g vercel
vercel link --yes --cwd frontend
vercel env add VITE_API_URL production "https://webcad-backend.onrender.com" --yes
vercel --prod --cwd frontend
```

## Switching LLM Providers

To switch between OpenAI and Anthropic, update the `LLM_PROVIDER` environment variable:

- `LLM_PROVIDER=openai` for OpenAI
- `LLM_PROVIDER=anthropic` for Anthropic

No code changes needed - just update the environment variable and redeploy.