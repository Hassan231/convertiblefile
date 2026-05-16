from flask import Flask, render_template, request, send_file
from pdf2docx import Converter
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = "converted"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/pdf-to-word", methods=["POST"])
def pdf_to_word():

    uploaded_file = request.files["file"]

    if uploaded_file.filename == "":
        return "No file selected"

    # Save uploaded PDF
    pdf_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    uploaded_file.save(pdf_path)

    # Output DOCX path
    word_filename = uploaded_file.filename.replace(".pdf", ".docx")
    word_path = os.path.join(CONVERTED_FOLDER, word_filename)

    # Convert PDF to Word
    cv = Converter(pdf_path)
    cv.convert(word_path)
    cv.close()

    # Send converted file
    return send_file(word_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
