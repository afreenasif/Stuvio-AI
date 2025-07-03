import os
from gtts import gTTS
from moviepy.editor import AudioFileClip, VideoFileClip
import google.generativeai as genai
from dotenv import load_dotenv
import re
from flask import Flask, render_template, request, redirect, url_for, session
from moviepy.audio.fx.all import audio_loop

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")

app = Flask(__name__)
app.secret_key = 'your_super_secret_and_long_random_key_here_1234567890' 

def generate_video(topic: str):
    print(f"[INFO] Generating video for topic: {topic}")

    prompt = f"Generate an engaging, plain-text voiceover script about '{topic}' for an educational video—no visuals, no narrator cues, just spoken content."
    response = model.generate_content(prompt)
    script = response.text.strip()

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

        if audio.duration < video.duration:
            print("[WARNING] Audio is shorter than video. Looping audio.")
            num_loops = int(video.duration / audio.duration) + 1
            audio = audio_loop(audio, duration=video.duration)
        elif audio.duration > video.duration:
            print("[WARNING] Audio is longer than video. Trimming audio.")
            audio = audio.subclip(0, video.duration)


        output_path = os.path.join("static", "output.mp4")
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        final_video = video.set_audio(audio)
        final_video.write_videofile(output_path, fps=video.fps)
        print(f"Moviepy - video ready {output_path}") 

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
                print(f"[ERROR] Could not remove voice.mp3: {e}. It might be in use.")

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

def parse_quiz_text(quiz_text: str):
    questions = []
    lines = quiz_text.split('\n')
    current_question = {}
    
    option_regex = re.compile(r'^[a-d]\)\s*(.*)')
    correct_answer_regex = re.compile(r'Correct Answer:\s*([a-d])\)\s*(.*)')

    question_counter = 0 

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith('Q') and '?' in line:
            if current_question:
                questions.append(current_question)
            question_counter += 1
            current_question = {
                'question_text': line,
                'options': [],
                'correct_answer_letter': '',
                'correct_answer_text': '',
                'question_index': question_counter 
            }
        elif option_match := option_regex.match(line):
            if current_question:
                option_letter = line[0]
                option_text = option_match.group(1).strip()
                current_question['options'].append({'letter': option_letter, 'text': option_text})
        elif correct_answer_match := correct_answer_regex.match(line):
            if current_question:
                current_question['correct_answer_letter'] = correct_answer_match.group(1).strip()
                current_question['correct_answer_text'] = correct_answer_match.group(2).strip()

    if current_question:
        questions.append(current_question)

    return questions

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    topic = request.form.get('prompt')
    if not topic:
        return render_template('index.html', error="Please provide a topic.")

    print(f"[INFO] Received topic for generation: {topic}")

    try:
        video_path = generate_video(topic)
        quiz_text = generate_quiz(topic)

        parsed_quiz = parse_quiz_text(quiz_text)

        session['video_url'] = '/' + video_path
        session['quiz_data'] = parsed_quiz
        session['topic'] = topic

        print(f"[INFO] Generation complete. Redirecting to video page.")
        return redirect(url_for('video_page'))
    except FileNotFoundError as e:
        print(f"[ERROR] File not found: {e}")
        return render_template('index.html', error=f"Error: {e}")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred during generation: {e}")
        return render_template('index.html', error=f"An error occurred during video/quiz generation. Please try again or check server logs.")

@app.route('/video')
def video_page():
    video_url = session.get('video_url', None)
    quiz_data_available = session.get('quiz_data', None) 
    topic = session.get('topic', 'your topic')

    if not video_url:
        print("[WARNING] video_url not found in session for /video. Redirecting to home.")
        return redirect(url_for('home'))

    return render_template('video_page.html',
                           video_url=video_url,
                           topic=topic,
                           quiz_available=True if quiz_data_available else False)

@app.route('/quiz')
def quiz_page():
    quiz_data = session.get('quiz_data', None)
    topic = session.get('topic', 'your topic')

    if not quiz_data:
        print("[WARNING] quiz_data not found in session for /quiz. Redirecting to home.")
        return redirect(url_for('home'))

    return render_template('quiz_page.html',
                           topic=topic,
                           questions=quiz_data)

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    if not os.path.exists('templates'):
        os.makedirs('templates')

    app.run(debug=True)