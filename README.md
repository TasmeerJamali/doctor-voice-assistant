# Doctor Voice Assistant 🩺🗣️

An AI-powered medical assistant that listens to patient voice input, analyzes facial images using a multimodal LLM, and responds with a professional doctor's voice. Built using Python, Gradio, ElevenLabs, Groq, and gTTS.

---

## 🚀 Features

- 🎤 **Speech-to-Text**: Converts patient's spoken input to text using Whisper (via Groq API)
- 🧠 **Image Diagnosis**: Analyzes uploaded images with a multimodal LLM (LLaMA via Groq) to simulate medical insight
- 🗣️ **Text-to-Speech**: Responds using AI-generated doctor's voice (via ElevenLabs or gTTS)
- 🌐 **Web Interface**: Clean and interactive Gradio-based UI for easy interaction

---

## 🛠️ Tech Stack

- **Gradio** – Web interface
- **Groq API** – LLM and Whisper (for text/image understanding and transcription)
- **ElevenLabs** – AI voice synthesis
- **gTTS** – Fallback or alternative text-to-speech
- **SpeechRecognition & PyDub** – Audio input and conversion
- **Python** – Core logic and backend

---

## 🖼️ Workflow Overview

1. **User speaks into mic**
2. **Audio transcribed to text**
3. **Image (if provided) is analyzed by the LLM**
4. **AI doctor replies with voice + text**

---

## 📁 Project Structure

```bash
├── voice_of_the_patient.py      # Records and transcribes voice input
├── voice_of_the_doctor.py       # Converts text response to speech
├── brain_of_the_doctor.py       # Image analysis with Groq's multimodal LLM
├── gradio_app.py                # Gradio UI for interaction
├── .env                         # API keys and secrets
├── requirements.txt             # Python dependencies
