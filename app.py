from flask import Flask, render_template, request
from langdetect import detect
from googletrans import Translator, LANGUAGES
import asyncio

app = Flask(__name__)

# Create an async function to handle the translation
async def detect_and_translate(text, target_lang):
    # Detect language
    result_lang = detect(text)

    # Translate language asynchronously
    translator = Translator()
    translated = await translator.translate(text, dest=target_lang)

    return result_lang, translated.text

# Flask route that synchronously calls the async function
@app.route('/')
def index():
    return render_template('index.html', languages=LANGUAGES)


@app.route('/trans', methods=['POST'])
def trans():
    translation = ""
    detected_lang = ""
    if request.method == 'POST':
        text = request.form['text']
        target_lang = request.form['target_lang']

        # Use asyncio.run() to run the async function
        detected_lang, translation = asyncio.run(detect_and_translate(text, target_lang))

    return render_template('index.html', translation=translation, detected_lang=detected_lang, languages=LANGUAGES)


if __name__ == '__main__':
    app.run(debug=True)
