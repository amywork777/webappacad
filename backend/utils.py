import subprocess, tempfile, pathlib, os
DOCKER_IMG = "webcad-fc"
TEST_MODE = os.environ.get("TEST_MODE", "false").lower() == "true"

def run_freecad_script(code: str, out="part.step"):
    with tempfile.TemporaryDirectory() as td:
        script = pathlib.Path(td)/"job.py"
        script.write_text(code)
        
        if TEST_MODE:
            # Test mode - just return a dummy file for testing
            output_file = pathlib.Path(td)/out
            output_file.write_text("This is a test STEP file content")
            print(f"TEST MODE: Simulating FreeCAD operation. Code: {code[:100]}...")
            return str(output_file)
        else:
            # Normal mode - use Docker
            cmd=["docker","run","--rm","-v",f"{td}:/w",DOCKER_IMG,
                "freecadcmd","/w/job.py"]
            subprocess.check_call(cmd)
            return str(pathlib.Path(td)/out)

def run_mcp(image: str, prompt: str):
    import pathlib, tempfile
    with tempfile.TemporaryDirectory() as td:
        out = pathlib.Path(td)/"mcp.step"
        
        if TEST_MODE:
            # Test mode - just return a dummy file for testing
            out.write_text(f"This is a test STEP file from MCP. Image: {image}, Prompt: {prompt}")
            print(f"TEST MODE: Simulating MCP operation. Image: {image}, Prompt: {prompt}")
            return str(out)
        else:
            # Normal mode - use Docker
            cmd=["docker","run","--rm",
                "-v",f"{pathlib.Path(image).parent}:/in",
                "-v",f"{td}:/out",DOCKER_IMG,
                "python3","/opt/mcp/examples/image2cad.py",
                "--image",f"/in/{pathlib.Path(image).name}",
                "--prompt",prompt,"--output","/out/mcp.step"]
            subprocess.check_call(cmd)
            return str(out)