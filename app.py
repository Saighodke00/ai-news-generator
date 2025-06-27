from flask import Flask, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/generate', methods=['POST'])
def generate_news_video():
    import main  # This should have main.main()
    try:
        main.main()
        return "✅ Video generation complete!"
    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
