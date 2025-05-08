import tempfile, pathlib, shutil, traceback, sys, os
from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv; load_dotenv()
from llm import ask_llm
from utils import run_freecad_script, run_mcp
from fem_script import fem_py

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROMPT_TMPL = ("You are a FreeCAD Python generator. "
               "Return ONLY Python code that builds the part in mm.\n\nDesign: {q}")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler to provide detailed error information"""
    error_detail = {
        "error": str(exc),
        "traceback": traceback.format_exception(type(exc), exc, exc.__traceback__)
    }
    print("ERROR:", error_detail)
    return JSONResponse(
        status_code=500,
        content={"detail": error_detail},
    )

@app.post("/api/generate")
async def gen_text(body: dict):
    try:
        print(f"Received prompt: {body['prompt']}")
        code = ask_llm(PROMPT_TMPL.format(q=body["prompt"]))
        print(f"Generated code (first 100 chars): {code[:100]}...")
        step = run_freecad_script(code)
        print(f"Created STEP file at: {step}")
        return FileResponse(step, filename="model.step")
    except Exception as e:
        print(f"Error in gen_text: {str(e)}")
        traceback.print_exc()
        raise

@app.post("/api/generate_from_image")
async def gen_img(file: UploadFile, prompt: str = Form("")):
    try:
        print(f"Received image file: {file.filename}, prompt: {prompt}")
        img = pathlib.Path("/tmp")/file.filename
        img.write_bytes(await file.read())
        print(f"Saved image to: {img}")
        step = run_mcp(str(img), prompt)
        print(f"Created STEP file at: {step}")
        return FileResponse(step, filename="image2cad.step")
    except Exception as e:
        print(f"Error in gen_img: {str(e)}")
        traceback.print_exc()
        raise

@app.post("/api/drawing")
async def drawing(body: dict):
    try:
        print(f"Received drawing request")
        src = pathlib.Path(tempfile.gettempdir())/'tmp.step'
        src.write_bytes(await (await body['step_url']).read())
        print(f"Saved STEP file to: {src}")
        pdf = run_freecad_script(f"""
import FreeCAD, Import, TechDraw
doc=FreeCAD.newDocument(); obj=Import.insert('{src}',doc.Name)
page=doc.addObject('TechDraw::DrawPage','Page')
tpl=doc.addObject('TechDraw::DrawSVGTemplate','Template')
tpl.Template=FreeCAD.getResourceDir()+'Mod/TechDraw/Templates/A4_Landscape.svg'
page.Template=tpl; view=doc.addObject('TechDraw::DrawViewPart','View')
view.Source=obj; page.addView(view); doc.recompute()
doc.TechDraw.exportPdf('{src}.pdf')
""", out="drawing.pdf")
        print(f"Created PDF file at: {pdf}")
        return FileResponse(pdf, filename="drawing.pdf")
    except Exception as e:
        print(f"Error in drawing: {str(e)}")
        traceback.print_exc()
        raise

@app.post("/api/fea")
async def fea(body: dict):
    try:
        print(f"Received FEA request with load: {body.get('load',100)}")
        src = pathlib.Path(tempfile.gettempdir())/'tmp.step'
        src.write_bytes(await (await body['step_url']).read())
        print(f"Saved STEP file to: {src}")
        vtk = run_freecad_script(fem_py(str(src), body.get('load',100)),
                                out="result.vtk")
        print(f"Created VTK file at: {vtk}")
        return FileResponse(vtk, filename="stress.vtk")
    except Exception as e:
        print(f"Error in fea: {str(e)}")
        traceback.print_exc()
        raise

@app.get("/api/test")
async def test_endpoint():
    """Simple test endpoint to verify the backend is working"""
    try:
        env_vars = {
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", "")[:5] + "..." if os.getenv("OPENAI_API_KEY") else None,
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY", "")[:5] + "..." if os.getenv("ANTHROPIC_API_KEY") else None,
            "LLM_PROVIDER": os.getenv("LLM_PROVIDER", ""),
            "TEST_MODE": os.getenv("TEST_MODE", "")
        }
        return {
            "status": "ok",
            "message": "Backend is working!",
            "environment": env_vars
        }
    except Exception as e:
        print(f"Error in test_endpoint: {str(e)}")
        traceback.print_exc()
        raise