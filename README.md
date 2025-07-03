# STUVIO.AI - AI-Powered Educational Video Generator

## Project Overview

STUVIO.AI is a full-stack AI web application designed to revolutionize personalized education by generating customized video content from user prompts. This platform automates the creation of educational videos complete with AI-generated scripts, realistic voiceovers, and avatar-based visuals, making learning more engaging and accessible.

---

## Features

* **Personalized Video Generation:** Create educational videos on various topics based on user-defined prompts.
* **AI-Driven Scripting:** Utilizes the Gemini API to intelligently generate comprehensive and coherent video scripts.
* **Realistic Voiceovers:** Integrates gTTS (Google Text-to-Speech) to convert scripts into natural-sounding audio.
* **Automated Avatar Animation:** Leverages MoviePy to automate the process of creating engaging, avatar-based educational videos.
* **Dynamic Quiz Generation:** Features AI-driven quiz generation to reinforce learning after video consumption.
* **Seamless User Interaction:** Developed with Flask APIs to ensure smooth management of video rendering, quiz creation, and overall user experience.

---

## Tech Stack

* **Backend:** Python, Flask
* **AI/Generative:** Gemini API
* **Video & Audio Processing:** MoviePy, gTTS (Google Text-to-Speech)
* **Version Control:** Git, GitHub

---
## Usage

1.  Navigate to the web application in your browser.
2.  Enter your educational prompt for the desired video content.
3.  The application will process the prompt, generate a script via Gemini API, create a voiceover, and compile the avatar-based video.
4.  Optionally, engage with AI-generated quizzes related to the video content.

---

## Setup and Local Installation

To run STUVIO.AI locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/afreenasif/Stuvio-AI.git](https://github.com/afreenasif/Stuvio-AI.git)
    cd Stuvio-AI
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # For Windows:
    .\venv\Scripts\activate
    # For macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(If you don't have a `requirements.txt` yet, you can create one by running `pip freeze > requirements.txt` after installing all your project's libraries like Flask, google-generative-ai, moviepy, gtts, etc.)*

4.  **Set up Gemini API Key:**
    * Obtain your API key from the [Google AI Studio](https://aistudio.google.com/app/apikey).
    * Create a `.env` file in the root directory of your project.
    * Add your API key to the `.env` file:
        ```
        GEMINI_API_KEY='your_gemini_api_key_here'
        ```
    * Ensure you have `python-dotenv` installed (`pip install python-dotenv`) and load it in your `app.py` or relevant script.

5.  **Run the Flask application:**
    ```bash
    flask run
    ```
    or if you have `app.py`:
    ```bash
    python app.py
    ```