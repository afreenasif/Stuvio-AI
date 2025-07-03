import os
from gtts import gTTS
from moviepy.editor import AudioFileClip, VideoFileClip
import google.generativeai as genai
from dotenv import load_dotenv
from moviepy.audio.fx.all import audio_loop

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")

def generate_video(topic: str):
    print(f"[INFO] Generating video for topic: {topic}")

    prompt = f"Generate an engaging, plain-text voiceover script about '{topic}' for an educational video—no visuals, no narrator cues, just spoken content."
    response = model.generate_content(prompt)
    script = response.text.strip()

    # Text-to-Speech
    tts = gTTS(text=script, lang='en')
    tts.save("voice.mp3")

    avatar_path = os.path.join("static", "avatar.mp4")
    if not os.path.exists(avatar_path):
        raise FileNotFoundError(f"Missing required file: {avatar_path}. Please place it in the 'static' folder.")

    video = None
    audio = None
    try:
        video = VideoFileClip(avatar_path)
        audio = AudioFileClip("voice.mp3")

        audio = audio.set_duration(video.duration)

        final_video = video.set_audio(audio)
        output_path = os.path.join("static", "output.mp4")
        final_video.write_videofile(output_path, fps=video.fps)

        return output_path
    except Exception as e:
        print(f"[ERROR] Error during video processing: {e}")
        raise
    finally:
        if audio:
            audio.close()
        if video:
            video.close()
        if os.path.exists("voice.mp3"):
            try:
                os.remove("voice.mp3")
                print("[INFO] Cleaned up temporary voice.mp3")
            except Exception as e:
                print(f"[ERROR] Could not remove voice.mp3: {e}")

def generate_quiz(topic: str):
    prompt = f"""
    Based on the topic '{topic}', generate a short quiz with 3 multiple-choice questions.
    For each question, list the options (a, b, c, d) and then on a new line, explicitly state the correct answer as 'Correct Answer: [option_letter]) [Option Text]'.

    Example format:

    Q1. What is the capital of France?
    a) London
    b) Paris
    c) Rome
    d) Berlin
    Correct Answer: b) Paris

    Q2. Which planet is known as the Red Planet?
    a) Earth
    b) Venus
    c) Mars
    d) Jupiter
    Correct Answer: c) Mars
    """
    response = model.generate_content(prompt)
    return response.text.strip()