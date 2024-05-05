from flask import Flask, render_template, request, jsonify
from g4f.client import Client
import speech_recognition as sr

app = Flask(__name__)
client = Client()

def chat_with_gpt(input_message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": input_message}],
        language="en", 
    )
    return response.choices[0].message.content

def convert_speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Please speak something...")
        recognizer.adjust_for_ambient_noise(source)  
        audio_data = recognizer.listen(source)  

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio_data)
        print(text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return ""
    except sr.RequestError as e:
        print("Sorry, there was an error processing your request. {0}".format(e))
        return ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    bot_response = chat_with_gpt(user_input)
    return jsonify({'bot_response': bot_response})

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    text = convert_speech_to_text()
    return jsonify({'text': text})

if __name__ == "__main__":
    app.run(debug=True)
