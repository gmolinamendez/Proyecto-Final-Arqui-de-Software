from pathlib import Path

from flask import Flask


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIST_DIR = BASE_DIR / "frontend" / "dist"
app = Flask(__name__)
