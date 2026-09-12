import os
from main.settings import default_input_dir as in_dir
from main.main import run_pipeline

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from pathlib import Path
import traceback

app = Flask(__name__)

UPLOAD_FOLDER = in_dir
ALLOWED_EXTENSIONS = ["pdf"]

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # Enforce a 16MB file limit

# Ensure the upload directory physically exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Validate file extensions securely."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    """Render the upload interface."""
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file segment found in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file was selected"}), 400

    if not (file and allowed_file(file.filename)):
        return jsonify({"error": "File type is not permitted"}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    try:
        # Run your actual pipeline synchronously, blocking the request
        # until the output workbook exists.
        output_path = run_pipeline(
            save_path
        )  # <-- your usp_parser/llm_handler/excel_writer chain
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Processing failed: {e}"}), 500

    # Send the finished file back as the response body itself
    return send_file(
        output_path,
        as_attachment=True,
        download_name=Path(output_path).name,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


if __name__ == "__main__":
    app.run(debug=True)


# ... existing config ...
