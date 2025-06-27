from fetch_headlines import fetch_headlines
from generate_audio import generate_single_audio
from fetch_images import fetch_single_image_pair
from make_video import create_clip, concatenate_videoclips, RESOLUTION
from moviepy.editor import CompositeAudioClip, AudioFileClip
import asyncio
import os

OUTPUT_VIDEO = "static/final_video.mp4"
BG_MUSIC = "static/bg_music.mp3"

async def process_headline_pipeline(index, headline, log):
    log.append(f"\n🔄 Processing Headline {index+1}: {headline}")

    audio_path = f"audio/headline_{index+1}.mp3"
    await generate_single_audio(headline, audio_path)
    log.append(f"🔊 Audio: {audio_path}")

    img1, img2 = fetch_single_image_pair(headline, index+1)
    log.append(f"🖼️ Images: {img1}, {img2}")

    clip = create_clip(img1, img2, audio_path, headline_text=headline)
    if clip:
        log.append(f"🎬 Clip Created")
    else:
        log.append(f"⚠️ Clip creation failed")
    return clip

async def main_pipeline():
    log = ["🚀 Starting Pipeline"]
    headlines = fetch_headlines()
    log.append(f"📰 Headlines Fetched: {len(headlines)}")

    tasks = [process_headline_pipeline(i, h, log) for i, h in enumerate(headlines)]
    clips = await asyncio.gather(*tasks)
    clips = [c for c in clips if c]

    if not clips:
        log.append("⚠️ No clips generated.")
        return "\n".join(log)

    final_video = concatenate_videoclips(clips)

    if os.path.exists(BG_MUSIC):
        try:
            bg = AudioFileClip(BG_MUSIC).volumex(0.1).subclip(0, final_video.duration)
            final_video = final_video.set_audio(CompositeAudioClip([final_video.audio, bg]))
            log.append("🎵 Background music added.")
        except Exception as e:
            log.append(f"⚠️ BG Music Error: {e}")

    if os.path.exists(OUTPUT_VIDEO):
        try:
            os.remove(OUTPUT_VIDEO)
        except:
            pass

    final_video.write_videofile(
        OUTPUT_VIDEO, codec="libx264", audio_codec="aac", fps=24,
        preset="ultrafast", threads=4, ffmpeg_params=["-crf", "26"]
    )

    log.append(f"✅ Video saved to: {OUTPUT_VIDEO}")
    return "\n".join(log)

if __name__ == "__main__":
    print(asyncio.run(main_pipeline()))
