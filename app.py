from jinja2 import filters
from pathlib import Path
from uuid import uuid4

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from config import Config


def allowed_pdf(file) -> bool:
    if not file.filename or "." not in file.filename:
        return False

    extension = file.filename.rsplit(".", 1)[1].lower()
    if extension != "pdf":
        return False

    # Verify the file begins with the standard PDF signature.
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

    file.save(upload_folder / stored_name)

    flash(f"{original_name} uploaded successfully.", "success")
    return redirect(url_for("index"))

@app.errorhandler(RequestEntityTooLarge)
def file_too_large(_error):
    flash("File is too large. Maximum upload size is 25 MB.", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)