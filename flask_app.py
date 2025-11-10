from flask import Flask, jsonify, send_file
import os
from datetime import datetime

# Import the tracker implementation (works in headless mode inside containers)
try:
    from app import FitnessTrackerApp, HEADLESS
except Exception:
    # If import fails, expose a minimal health endpoint anyway
    FitnessTrackerApp = None
    HEADLESS = True

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify(status="ok")

@app.route("/generate")
def generate():
    """Generate the progress chart using the headless path and return the PNG.
    This endpoint is intended for containerized use where a GUI is not available.
    """
    outdir = os.getenv("HEADLESS_OUTPUT_DIR", ".")
    os.makedirs(outdir, exist_ok=True)

    if FitnessTrackerApp is None:
        return jsonify(error="tracker unavailable"), 500

    tracker = FitnessTrackerApp(None)
    # Optional: if no data exists, populate a small sample so a chart is produced
    if not any(tracker.workouts.values()):
        tracker.workouts = {
            "Warm-up": [{"exercise": "Jumping Jacks", "duration": 5, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}],
            "Workout": [{"exercise": "Squats", "duration": 30, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}],
            "Cool-down": [{"exercise": "Stretching", "duration": 5, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]
        }

    # This will save a PNG when running headless
    tracker.update_progress_charts()

    # Find the most recent generated file
    files = [f for f in os.listdir(outdir) if f.startswith("progress_") and f.endswith('.png')]
    if not files:
        return jsonify(error="no file generated"), 500
    latest = max(files)
    path = os.path.join(outdir, latest)
    return send_file(path, mimetype='image/png')
