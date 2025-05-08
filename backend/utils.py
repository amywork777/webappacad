import subprocess, tempfile, pathlib, os, shutil
DOCKER_IMG = "webcad-fc"
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"
# Create a directory to store temporary files that need to persist
TEMP_DIR = pathlib.Path(tempfile.gettempdir()) / "webcad_temp"
os.makedirs(TEMP_DIR, exist_ok=True)

def run_freecad_script(code: str, out="part.step"):
    with tempfile.TemporaryDirectory() as td:
        script = pathlib.Path(td)/"job.py"
        script.write_text(code)
        
        if TEST_MODE:
            # Test mode - just return a dummy file for testing
            output_file = pathlib.Path(td)/out
            output_file.write_text("This is a test STEP file content")
            print(f"TEST MODE: Simulating FreeCAD operation. Code: {code[:100]}...")
            
            # Copy to a more permanent location
            permanent_file = TEMP_DIR / f"test_{pathlib.Path(out).name}"
            shutil.copy2(output_file, permanent_file)
            print(f"Copied output to permanent location: {permanent_file}")
            return str(permanent_file)
        else:
            # Normal mode - use Docker
            cmd=["docker","run","--rm","-v",f"{td}:/w",DOCKER_IMG,
                "freecadcmd","/w/job.py"]
            subprocess.check_call(cmd)
            
            # Copy to a more permanent location
            permanent_file = TEMP_DIR / f"docker_{pathlib.Path(out).name}"
            shutil.copy2(pathlib.Path(td)/out, permanent_file)
            return str(permanent_file)

def run_mcp(image: str, prompt: str):
    with tempfile.TemporaryDirectory() as td:
        out = pathlib.Path(td)/"mcp.step"
        
        if TEST_MODE:
            # Test mode - just return a dummy file for testing
            out.write_text(f"This is a test STEP file from MCP. Image: {image}, Prompt: {prompt}")
            print(f"TEST MODE: Simulating MCP operation. Image: {image}, Prompt: {prompt}")
            
            # Copy to a more permanent location
            permanent_file = TEMP_DIR / f"test_mcp_{pathlib.Path(image).name}.step"
            shutil.copy2(out, permanent_file)
            print(f"Copied output to permanent location: {permanent_file}")
            return str(permanent_file)
        else:
            # Normal mode - use Docker
            cmd=["docker","run","--rm",
                "-v",f"{pathlib.Path(image).parent}:/in",
                "-v",f"{td}:/out",DOCKER_IMG,
                "python3","/opt/mcp/examples/image2cad.py",
                "--image",f"/in/{pathlib.Path(image).name}",
                "--prompt",prompt,"--output","/out/mcp.step"]
            subprocess.check_call(cmd)
            
            # Copy to a more permanent location
            permanent_file = TEMP_DIR / f"docker_mcp_{pathlib.Path(image).name}.step"
            shutil.copy2(out, permanent_file)
            return str(permanent_file)