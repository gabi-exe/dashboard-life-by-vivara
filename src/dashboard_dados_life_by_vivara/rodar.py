import os
import subprocess
import sys

PASTA = os.path.dirname(os.path.abspath(__file__))

try:
    subprocess.run(
        [
            sys.executable, "-m", "streamlit", "run", os.path.join(PASTA, "dashboard.py"),
            "--theme.base", "light",
            "--theme.primaryColor", "#B8860B",
            "--theme.backgroundColor", "#FAF7F5",
            "--theme.secondaryBackgroundColor", "#FFFFFF",
            "--theme.textColor", "#1c1917",
            "--browser.gatherUsageStats", "false",
        ],
        cwd=PASTA,
    )
except KeyboardInterrupt:
    pass
