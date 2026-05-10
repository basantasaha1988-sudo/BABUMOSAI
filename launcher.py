import subprocess
import time
import os
import sys

# --------------------------------
# GET BASE DIRECTORY
# --------------------------------
if getattr(sys, 'frozen', False):

    BASE_DIR = os.path.dirname(sys.executable)

else:

    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

# --------------------------------
# FILE PATHS
# --------------------------------
backend_file = os.path.join(
    BASE_DIR,
    "backend.py"
)

frontend_file = os.path.join(
    BASE_DIR,
    "frontend.py"
)

# --------------------------------
# START BACKEND
# --------------------------------
backend = subprocess.Popen(
    [
        "python",
        backend_file
    ],
    cwd=BASE_DIR
)

print("✅ Backend Started")

# WAIT
time.sleep(3)

# --------------------------------
# START FRONTEND
# --------------------------------
frontend = subprocess.Popen(
    [
        "python",
        "-m",
        "streamlit",
        "run",
        frontend_file,
        "--server.port=8501",
        "--server.address=0.0.0.0",
        "--server.headless=true"
    ],
    cwd=BASE_DIR
)

print("✅ Frontend Started")

# --------------------------------
# WAIT
# --------------------------------
try:

    frontend.wait()

except KeyboardInterrupt:

    print("🛑 Closing Game")

finally:

    backend.kill()

    print("✅ Backend Closed")