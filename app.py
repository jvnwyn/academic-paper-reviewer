from pathlib import Path
from uuid import uuid4

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from config import Config
from services.pdf_service import extract_text_from_pdf
from services.chunking_service import chunk_pages
from services.embedding_service import generate_embeddings
from services.vector_service import store_document_chunks
from services.gemini_service import GeminiServiceError
from services.rag_service import answer_question


def allowed_pdf(file: FileStorage) -> bool:
    filename = file.filename

    if filename is None or "." not in filename:
        return False

    if filename.rsplit(".", 1)[1].lower() != "pdf":
        return False

    header = file.stream.read(5)
    file.stream.seek(0)

    return header == b"%PDF-"


app = Flask(__name__)
app.config.from_object(Config)

upload_folder = Path(app.config["UPLOAD_FOLDER"])
upload_folder.mkdir(parents=True, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_pdf():
    file = request.files.get("paper")

    if file is None:
        flash("Please choose a PDF file.", "error")
        return redirect(url_for("index"))

    filename = file.filename

    if filename is None or filename == "":
        flash("Please choose a PDF file.", "error")
        return redirect(url_for("index"))

    if not allowed_pdf(file):
        flash("Only valid PDF files are allowed.", "error")
        return redirect(url_for("index"))

    original_name = secure_filename(filename)
    stored_name = f"{uuid4().hex}_{original_name}"

    file_path = upload_folder / stored_name
    file.save(file_path)

    try:
        extracted_pages = extract_text_from_pdf(file_path)
    except ValueError as error:
        file_path.unlink(missing_ok=True)
        flash(str(error), "error")
        return redirect(url_for("index"))

    if not extracted_pages:
        flash(
            "The PDF uploaded, but no readable text was found. "
            "It may be a scanned document.",
            "error",
        )
        return redirect(url_for("index"))
    
    chunks = chunk_pages(extracted_pages)
    embedded_chunks = generate_embeddings(chunks)
    stored_count = store_document_chunks(
        embedded_chunks,
        original_name,
    )

    session["current_file"] = original_name

    flash(
        f"{original_name} uploaded successfully. "
        f"Extracted text from {len(extracted_pages)} page(s), "
        f"created {len(chunks)} chunk(s), generated "
        f"{len(embedded_chunks)} embedding vector(s), and stored "
        f"{stored_count} chunk(s) in ChromaDB.",
        "success",
    )
    return redirect(url_for("index"))

@app.route("/ask", methods=["POST"])
def ask_question():
    question = request.form.get("question", "").strip()
    file_name = session.get("current_file")

    if not question:
        flash("Please enter a question.", "error")
        return redirect(url_for("index"))

    if not isinstance(file_name, str):
        flash("Upload a PDF before asking a question.", "error")
        return redirect(url_for("index"))

    try:
        rag_response = answer_question(question, file_name)
    except GeminiServiceError as error:
        flash(str(error), "error")
        return redirect(url_for("index"))

    return render_template(
        "index.html",
        question=question,
        answer=rag_response["answer"],
        results=rag_response["sources"],
    )

@app.errorhandler(RequestEntityTooLarge)
def file_too_large(_error):
    flash("File is too large. Maximum upload size is 25 MB.", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)