from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import asyncio
import main  # your main_pipeline code is inside main.py

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate.html")
def generate_page():
    return render_template("generate.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        log = asyncio.run(main.main_pipeline())  # Run the async video generation pipeline
        return jsonify({"status": "success", "log": log})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/video")
def video():
    return app.send_static_file("final_video.mp4")

if __name__ == "__main__":
    app.run(debug=True)
