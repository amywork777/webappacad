import subprocess, tempfile, pathlib
DOCKER_IMG = "webcad-fc"

def run_freecad_script(code: str, out="part.step"):
    with tempfile.TemporaryDirectory() as td:
        script = pathlib.Path(td)/"job.py"
        script.write_text(code)
        cmd=["docker","run","--rm","-v",f"{td}:/w",DOCKER_IMG,
             "freecadcmd","/w/job.py"]
        subprocess.check_call(cmd)
        return str(pathlib.Path(td)/out)

def run_mcp(image: str, prompt: str):
    import pathlib, tempfile
    with tempfile.TemporaryDirectory() as td:
        out = pathlib.Path(td)/"mcp.step"
        cmd=["docker","run","--rm",
             "-v",f"{pathlib.Path(image).parent}:/in",
             "-v",f"{td}:/out",DOCKER_IMG,
             "python3","/opt/mcp/examples/image2cad.py",
             "--image",f"/in/{pathlib.Path(image).name}",
             "--prompt",prompt,"--output","/out/mcp.step"]
        subprocess.check_call(cmd)
        return str(out)