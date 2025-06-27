import os
import asyncio
import edge_tts
import re

# 🎙️ Voice Options
VOICE_OPTIONS = {
    "Hindi Female": "hi-IN-SwaraNeural",
    "Hindi Male": "hi-IN-MadhurNeural",
    "English (India) Female": "en-IN-NeerjaNeural",
    "English (India) Male": "en-IN-PrabhatNeural",
    "Marathi Female": "mr-IN-AarohiNeural",
    "Marathi Male": "mr-IN-ManoharNeural",
    "English (US) Female": "en-US-JennyNeural",
    "English (US) Male": "en-US-GuyNeural"
}

# 🗣️ Default Voice
SELECTED_VOICE = VOICE_OPTIONS["Hindi Female"]
AUDIO_FOLDER = "audio"

# 🔐 Safe Filename Helper
def sanitize_filename(text):
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', text.strip())[:50]

# ✅ NEW: Single-audio async generator (used in pipeline)
async def generate_single_audio(text, output_path, voice=SELECTED_VOICE):
    try:
        tts = edge_tts.Communicate(text=text, voice=voice)
        await tts.save(output_path)
        print(f"🎧 Audio saved: {output_path}")
    except Exception as e:
        print(f"❌ Error generating audio: {text}\n{e}")

# 🔁 Legacy batch mode (still works)
async def generate_audio_per_headline(headlines, audio_folder=AUDIO_FOLDER, voice=SELECTED_VOICE):
    if not headlines:
        print("⚠️ No headlines to convert to audio.")
        return

    os.makedirs(audio_folder, exist_ok=True)
    for file in os.listdir(audio_folder):
        if file.endswith(".mp3"):
            os.remove(os.path.join(audio_folder, file))

    print(f"\n🎤 Generating audio for {len(headlines)} headlines using voice: {voice}\n")

    tasks = []
    for i, headline in enumerate(headlines, 1):
        filename = os.path.join(audio_folder, f"headline_{i}.mp3")
        tasks.append(generate_single_audio(headline, filename, voice))

    await asyncio.gather(*tasks)
    print("\n✅ All headlines converted to audio.\n")

# 🧪 For testing
if __name__ == "__main__":
    from fetch_headlines import fetch_headlines
    headlines = fetch_headlines()
    asyncio.run(generate_audio_per_headline(headlines))
