from flask import Flask, render_template, request
from flask import send_file, redirect, url_for
from pdf2docx import Converter
import os
import uuid
from PIL import Image
import pythoncom
from docx2pdf import convert

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = "converted"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)




#----------------1-----------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/pdf-to-word', methods=['GET', 'POST'])
def pdf_to_word():
    # OPEN PAGE
    if request.method == 'GET':
        return render_template('pdf_to_word.html')

    uploaded_file = request.files["pdf"]

    if uploaded_file.filename == "":
        return "No file selected"

    # Save uploaded PDF
    pdf_path = os.path.join(
        UPLOAD_FOLDER,
        uploaded_file.filename
    )

    uploaded_file.save(pdf_path)

    # Output DOCX path
    word_filename = uploaded_file.filename.replace(
        ".pdf",
        ".docx"
    )

    word_path = os.path.join(
        CONVERTED_FOLDER,
        word_filename
    )

    # Convert PDF to Word
    cv = Converter(pdf_path)
    cv.convert(word_path)
    cv.close()

    # Send converted file
    return send_file(
        word_path,
        as_attachment=True
    )

@app.route('/image-converter', methods=['GET', 'POST'])
def image_converter():

    # OPEN PAGE
    if request.method == 'GET':

        return render_template(
            'image_converter.html'
        )

    # GET FILE
    file = request.files['image']

    # GET FORMAT
    output_format = request.form['format']

    # CHECK FILE
    if file.filename == "":

        return "No file selected"

    # OPEN IMAGE
    img = Image.open(file)

    # FIX TRANSPARENCY
    if output_format in ['jpg', 'jpeg']:

        if img.mode in ('RGBA', 'LA', 'P'):

            background = Image.new(
                "RGB",
                img.size,
                (255, 255, 255)
            )

            if img.mode == 'P':

                img = img.convert('RGBA')

            background.paste(
                img,
                mask=img.split()[-1]
            )

            img = background

        else:

            img = img.convert("RGB")

    # OUTPUT NAME
    filename = (
        str(uuid.uuid4())
        + "."
        + output_format
    )

    # OUTPUT PATH
    output_path = os.path.join(
        CONVERTED_FOLDER,
        filename
    )

    # FIX FORMAT NAME
    save_format = output_format.upper()

    if save_format == "JPG":

        save_format = "JPEG"

    # SAVE IMAGE
    img.save(
        output_path,
        save_format
    )

    # DOWNLOAD
    return send_file(
        output_path,
        as_attachment=True
    )
@app.route('/word-to-pdf', methods=['GET', 'POST'])
def word_to_pdf():

    # OPEN PAGE
    if request.method == 'GET':
        return render_template(
            'word_to_pdf.html'
        )

    # GET FILE
    uploaded_file = request.files['word']

    # CHECK FILE
    if uploaded_file.filename == "":
        return "No file selected"

    # SAVE PATH
    word_path = os.path.join(
        UPLOAD_FOLDER,
        uploaded_file.filename
    )

    # SAVE FILE
    uploaded_file.save(word_path)

    # PDF NAME
    pdf_filename = uploaded_file.filename.replace(
        ".docx",
        ".pdf"
    )

    # PDF PATH
    pdf_path = os.path.join(
        CONVERTED_FOLDER,
        pdf_filename
    )
    pythoncom.CoInitialize()
    # CONVERT
    try:

        convert(word_path, pdf_path)

    except Exception as e:

        return "Conversion Error: " + str(e)

    # DOWNLOAD
    return send_file(
        pdf_path,
        as_attachment=True
    )

if __name__ == '__main__':
    app.run(debug=True)