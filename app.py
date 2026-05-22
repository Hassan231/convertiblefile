from flask import Flask, render_template, request
from flask import send_file, redirect, url_for
from pdf2docx import Converter
import os
import uuid
from PIL import Image

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

@app.route('/jpg-to-pdf', methods=['GET', 'POST'])
def jpg_to_pdf():

    if request.method == 'GET':
        return render_template('jpg_to_pdf.html')

    file = request.files['image']

    ext = file.filename.lower().split('.')[-1]

    if ext not in ['jpg', 'jpeg', 'png']:
        return "Only JPG and PNG allowed"

    img = Image.open(file)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    os.makedirs("converted", exist_ok=True)

    filename = str(uuid.uuid4()) + ".pdf"
    output_path = os.path.join("converted", filename)

    img.save(output_path, "PDF")

    return send_file(output_path, as_attachment=True)

# ================= WORD TO PDF =================
@app.route('/word-to-pdf', methods=['GET', 'POST'])
def word_to_pdf():

    if request.method == 'GET':
        return render_template(
            'word_to_pdf.html'
        )

    uploaded_file = request.files['word']

    if uploaded_file.filename == "":
        return "No file selected"

    filename = uploaded_file.filename

    save_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    uploaded_file.save(save_path)

    return redirect(
        url_for(
            'workspace',
            tool='word-to-pdf',
            filename=filename
        )
    )


# ================= UNIVERSAL WORKSPACE =================
@app.route('/workspace/<tool>/<filename>')
def workspace(tool, filename):

    return render_template(
        'converter_workspace.html',
        tool=tool,
        filename=filename
    )
if __name__ == '__main__':
    app.run(debug=True)