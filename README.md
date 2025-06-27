# 🎥 AI News Generator

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-WebApp-000000?logo=flask)](https://flask.palletsprojects.com/)
[![MoviePy](https://img.shields.io/badge/MoviePy-VideoEditing-orange?logo=video)](https://zulko.github.io/moviepy/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> ⚡ Turn real-time news headlines into fully AI-generated videos using text-to-speech, automated image fetching, and visual effects — all in one click.

---

## 🚀 Features

- 🔍 Fetches latest headlines via custom scraper or API
- 🗣️ Converts text to AI voice using `edge-tts`
- 🖼️ Grabs relevant images via web scraping or Bing API
- 🎬 Creates engaging videos with transitions (MoviePy)
- 🎵 Background music support
- 🌐 Clean frontend UI built with Tailwind CSS and Lottie animations
- 📁 Auto-organized output and assets

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Flask**
- **MoviePy**
- **Edge-TTS**
- **aiohttp / requests**
- **HTML + Tailwind CSS**
- **JavaScript + Lottie**

---

## 🧪 Demo

> 🎬 [Click here to watch a sample video](#) <!-- replace with your YouTube link or hosted video -->
>  
> 🌐 [Live Web App (Coming Soon)](https://saighodke00.github.io/ai-news-generator)

---

## ⚙️ Installation

```bash
# Clone the repo
git clone https://github.com/Saighodke00/ai-news-generator.git
cd ai-news-generator

# Create virtual environment
python -m venv venv
venv\Scripts\activate   # On Windows

# Install requirements
pip install -r requirements.txt

# Run the server
python server.py
```

## 📂 Folder Structure
```
ai-news-generator/
├── backend/
│ ├── fetch_headlines.py
│ ├── fetch_images.py
│ ├── generate_audio.py
│ ├── make_video.py
│ └── server.py
├── static/
│ ├── final_video.mp4
│ └── bg_music.mp3
├── templates/
│ ├── index.html
│ ├── generate.html
│ └── gallery.html
├── requirements.txt
└── README.md
```
---

## 💡 To-Do / Ideas
 GitHub Pages deployment for frontend

 Add user input for custom topics

 Add more visual effects (Ken Burns, zoom-in)

 Implement multi-language voice options

 Save logs and analytics
 
 ---

---

## 👥 Contributors

| Name | Role | GitHub | Gmail |
|------|------|--------|-------|
| Sai Narendra Ghodke | Backend & Video Automation | [@Saighodke00](https://github.com/Saighodke00) |saighodke09@gmail.com|
| Aditay Salunkhe | Frontend UI & Design | [Messi0898](https://github.com/Messi0898) |aditaysalunkhe2550@gamil.com |

 
---

📄 License
This project is licensed under the MIT License

---

