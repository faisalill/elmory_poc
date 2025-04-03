from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import subprocess
import re

app = FastAPI()
svelte_build_dir = "../frontend/build"


@app.get("/list-files")
async def list_files():
    try:
        files = [f.name for f in Path("./").iterdir() if f.is_file()]
        return JSONResponse(content={"files": files})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/getacl")
async def get_acl(request: Request):
    data = await request.json()
    try:
        file_path = Path("./") / data["filename"]
        if not file_path.exists():
            return JSONResponse(content={"error": "File not found"}, status_code=404)

        acl = getfacl(file_path)
        return JSONResponse(content={"acl": acl})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/setacl")
async def set_acl(request: Request):
    data = await request.json()
    try:
        file_path = Path("./") / data["filename"]
        if not file_path.exists():
            return JSONResponse(content={"error": "File not found"}, status_code=404)

        res = setacl(file_path, data["user"], data["permissions"])
        return JSONResponse(content={"Result": res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


app.mount("/", StaticFiles(directory=svelte_build_dir, html=True), name="static")


def setacl(filepath, user, permissions):
    cmd = ["setfacl", "-m", f"u:{user}:{permissions}", str(filepath)]
    try:
        subprocess.run(cmd, check=True)
        return "Changed Permissions Successfully"
    except subprocess.CalledProcessError as e:
        return f"Error getting ACL: {e.stderr}"


def getfacl(filepath):
    cmd = ["getfacl", str(filepath)]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return parse_acl(result.stdout)
    except subprocess.CalledProcessError as e:
        return f"Error getting ACL: {e.stderr}"


def parse_acl(acl_output):
    acl_data = {"owner": None, "group": None, "entries": [], "default_entries": []}

    lines = acl_output.strip().split("\n")

    for line in lines:
        if line.startswith("# owner:"):
            acl_data["owner"] = line.split(":")[-1].strip()
        elif line.startswith("# group:"):
            acl_data["group"] = line.split(":")[-1].strip()

        match = re.match(
            r"(default:)?(user|group|other|mask):([\w-]*):?([rwx-]*)", line
        )
        if match:
            is_default = bool(match.group(1))
            acl_type = match.group(2)
            identity = match.group(3) if match.group(3) else None
            permissions = match.group(4)

            entry = {"type": acl_type, "identity": identity, "permissions": permissions}

            if is_default:
                acl_data["default_entries"].append(entry)
            else:
                acl_data["entries"].append(entry)

    return acl_data
