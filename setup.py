import os
import sys
import subprocess
import venv

env_dir = "venv_run"
python_exec = os.path.join(env_dir, "bin", "python")

if not os.path.exists(env_dir):
    venv.create(env_dir, with_pip=True)
    print("Virtualenv created:", env_dir)

subprocess.check_call([python_exec, "-m", "pip", "install", "--upgrade", "pip"])
subprocess.check_call([python_exec, "-m", "pip", "install", "requests", "python-dotenv"])
print("Dependencies installed in", env_dir)
