import os
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"

from moviepy.editor import (
    ImageClip, AudioFileClip, TextClip,
    CompositeAudioClip, CompositeVideoClip, concatenate_videoclips
)
from PIL import Image, UnidentifiedImageError

# ========== CONFIG ==========
FAST_MODE = True  # ⚡ Toggle this to False for full-quality render

RESOLUTION = (640, 360) if FAST_MODE else (1280, 720)
FPS = 24
THREADS = 2 if FAST_MODE else 4
IMAGE_FOLDER = "news_images"
AUDIO_FOLDER = "audio"
BG_MUSIC_PATH = "static/bg_music.mp3"
DEFAULT_OUTPUT_PATH = "static/final_video.mp4"
# ============================

def validate_and_clean_images(folder=IMAGE_FOLDER):
    print("🧼 Validating and cleaning images...")
    for filename in os.listdir(folder):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        path = os.path.join(folder, filename)
        try:
            with Image.open(path) as img:
                img = img.convert("RGB")
                img.load()
                if img.width < 400 or img.height < 300:
                    raise ValueError("Too small")
                img.save(path, format="JPEG", quality=90)
                print(f"✅ Cleaned: {filename}")
        except (UnidentifiedImageError, OSError, ValueError) as e:
            print(f"❌ Removed: {filename} → {e}")
            os.remove(path)

def safe_image(path):
    try:
        with Image.open(path) as img:
            img.load()
            return img.width >= 400 and img.height >= 300
    except:
        return False

def simple_zoom(image_path, duration, zoom_type="in"):
    clip = ImageClip(image_path).resize(width=RESOLUTION[0])
    if zoom_type == "in":
        clip = clip.crop(x1=30, y1=20, x2=clip.w - 30, y2=clip.h - 20).resize(RESOLUTION)
    else:
        clip = clip.crop(x1=0, y1=0, x2=clip.w - 30, y2=clip.h - 20).resize(RESOLUTION)
    return clip.set_duration(duration)

def create_clip(img1, img2, audio_path, headline_text=""):
    if not all(map(safe_image, [img1, img2])):
        return None
    try:
        audio = AudioFileClip(audio_path)
        total_duration = audio.duration
        dur1 = total_duration * 0.5
        dur2 = total_duration - dur1

        clip1 = simple_zoom(img1, dur1 + 0.5, "in")
        clip2 = simple_zoom(img2, dur2 + 0.5, "out").set_start(dur1)

        if not FAST_MODE:
            clip1 = clip1.fadeout(0.5)
            clip2 = clip2.fadein(0.5)

        base_clip = CompositeVideoClip([clip1, clip2], size=RESOLUTION).set_duration(total_duration)

        if headline_text:
            txt_clip = (
                TextClip(headline_text, fontsize=36, color='white', font='Arial-Bold', method='label')
                .set_position(("center", "bottom"))
                .set_duration(total_duration)
            )
            if not FAST_MODE:
                txt_clip = txt_clip.fadein(0.3).fadeout(0.3)

            base_clip = CompositeVideoClip([base_clip, txt_clip])

        return base_clip.set_audio(audio)

    except Exception as e:
        print(f"❌ Clip error with {img1}, {img2}: {e}")
        return None

def create_news_video(output_path=DEFAULT_OUTPUT_PATH):
    print(f"\n🎬 Starting news video generation → {'FAST MODE' if FAST_MODE else 'FULL MODE'}\n")
    validate_and_clean_images()

    audio_files = sorted([f for f in os.listdir(AUDIO_FOLDER) if f.endswith(".mp3")])
    clips = []

    for i, audio_file in enumerate(audio_files):
        img1 = os.path.join(IMAGE_FOLDER, f"img{i+1}_1.jpg")
        img2 = os.path.join(IMAGE_FOLDER, f"img{i+1}_2.jpg")
        audio = os.path.join(AUDIO_FOLDER, audio_file)
        headline = f"Top Headline {i+1}"

        print(f"🖼️ Processing: {os.path.basename(img1)}, {os.path.basename(img2)} + 🔊 {audio_file}")
        clip = create_clip(img1, img2, audio, headline)
        if clip:
            clips.append(clip)

    if not clips:
        print("⚠️ No valid clips created. Exiting.")
        return

    final_video = concatenate_videoclips(clips)

    if not FAST_MODE and os.path.exists(BG_MUSIC_PATH):
        try:
            bg = AudioFileClip(BG_MUSIC_PATH).volumex(0.1).subclip(0, final_video.duration)
            final_video = final_video.set_audio(CompositeAudioClip([final_video.audio, bg]))
            print("🎵 Background music layered in.")
        except Exception as e:
            print(f"⚠️ Background music skipped: {e}")

    # Force overwrite: always use the same output file
    if os.path.exists(output_path):
        try:
            os.remove(output_path)
        except Exception as e:
            print(f"⚠️ Couldn't remove old output: {e}")

    try:
        print(f"\n💾 Rendering to → {output_path} (overwrite mode)")
        final_video.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            fps=FPS,
            threads=THREADS,
            preset="ultrafast" if FAST_MODE else "veryfast",
            ffmpeg_params=["-crf", "26"] if FAST_MODE else ["-crf", "23"],
            remove_temp=True
        )
        print(f"\n✅ Final video saved: {output_path}\n")
    except Exception as e:
        print(f"❌ Rendering failed: {e}")

if __name__ == "__main__":
    create_news_video()
