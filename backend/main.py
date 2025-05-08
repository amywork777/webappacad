import tempfile, pathlib, shutil
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
from dotenv import load_dotenv; load_dotenv()
from llm import ask_llm
from utils import run_freecad_script, run_mcp
from fem_script import fem_py

app = FastAPI()
PROMPT_TMPL = ("You are a FreeCAD Python generator. "
               "Return ONLY Python code that builds the part in mm.\n\nDesign: {q}")

@app.post("/api/generate")
async def gen_text(body: dict):
    code = ask_llm(PROMPT_TMPL.format(q=body["prompt"]))
    step = run_freecad_script(code)
    return FileResponse(step, filename="model.step")

@app.post("/api/generate_from_image")
async def gen_img(file: UploadFile, prompt: str = Form("")):
    img = pathlib.Path("/tmp")/file.filename
    img.write_bytes(await file.read())
    step = run_mcp(str(img), prompt)
    return FileResponse(step, filename="image2cad.step")

@app.post("/api/drawing")
async def drawing(body: dict):
    src = pathlib.Path(tempfile.gettempdir())/'tmp.step'
    src.write_bytes(await (await body['step_url']).read())
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
    return FileResponse(pdf, filename="drawing.pdf")

@app.post("/api/fea")
async def fea(body: dict):
    src = pathlib.Path(tempfile.gettempdir())/'tmp.step'
    src.write_bytes(await (await body['step_url']).read())
    vtk = run_freecad_script(fem_py(str(src), body.get('load',100)),
                             out="result.vtk")
    return FileResponse(vtk, filename="stress.vtk")