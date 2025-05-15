import os
from flask import Flask, render_template_string, request, send_file, redirect, url_for
from dotenv import load_dotenv
load_dotenv()

from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs

system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. \
            What's in this image?. Do you find anything wrong with it medically? \
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in \
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.\
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'\
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, \
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

app = Flask(__name__)

HTML = '''
<!doctype html>
<title>AI Doctor with Vision and Voice</title>
<h1>AI Doctor with Vision and Voice</h1>
<form method=post enctype=multipart/form-data>
  <label>Upload your voice (mp3/wav/m4a):</label><br>
  <input type=file name=audio_file accept="audio/*"><br><br>
  <label>Upload an image (jpg/png):</label><br>
  <input type=file name=image_file accept="image/*"><br><br>
  <input type=submit value="Get Doctor's Response">
</form>
{% if speech_to_text_output %}
  <h3>Speech to Text</h3>
  <textarea rows=3 cols=80 readonly>{{ speech_to_text_output }}</textarea>
{% endif %}
{% if doctor_response %}
  <h3>Doctor's Response</h3>
  <textarea rows=3 cols=80 readonly>{{ doctor_response }}</textarea>
{% endif %}
{% if audio_url %}
  <h3>Doctor's Voice</h3>
  <audio controls src="{{ audio_url }}"></audio>
{% endif %}
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    speech_to_text_output = ''
    doctor_response = ''
    audio_url = None
    if request.method == 'POST':
        audio_file = request.files.get('audio_file')
        image_file = request.files.get('image_file')
        if audio_file:
            audio_path = 'temp_audio.mp3'
            audio_file.save(audio_path)
            speech_to_text_output = transcribe_with_groq(
                GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
                audio_filepath=audio_path,
                stt_model="whisper-large-v3"
            )
        if image_file:
            image_path = 'temp_image.jpg'
            image_file.save(image_path)
            doctor_response = analyze_image_with_query(
                query=system_prompt + (speech_to_text_output or ""),
                encoded_image=encode_image(image_path),
                model="llama-3.3-70b-versatile"
            )
        else:
            doctor_response = "No image provided for me to analyze"
        audio_path_out = text_to_speech_with_elevenlabs(
            input_text=doctor_response,
            output_filepath="final.mp3"
        )
        audio_url = url_for('get_audio')
    return render_template_string(HTML, speech_to_text_output=speech_to_text_output, doctor_response=doctor_response, audio_url=audio_url)

@app.route('/audio')
def get_audio():
    return send_file('final.mp3', mimetype='audio/mp3')

if __name__ == '__main__':
    app.run(debug=True) 