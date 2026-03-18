from flask import Flask, Response, jsonify, request
from werkzeug.utils import secure_filename
import os
from file_storage import download_from_s3, upload_to_s3
from utils import allowed_file, valid_code

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1000 * 1000  # MAX Limit of file 5 MB


@app.route("/upload", methods=["POST"])
def upload():
    code = 1000
    if "file" not in request.files:
        return jsonify({"status": "error", "message": "file was not the path"})

    file = request.files["file"]
    if file.filename == "" or file.filename is None:
        return jsonify({"status": "error", "message": "No file was selected"})

    print(file)
    filename = secure_filename(file.filename)
    if not allowed_file(filename):
        return jsonify(
            {
                "status": "error",
                "message": "Supported format for now are .txt, .pdf, .png, .jpg, .jpeg, .gif",
            },
        )

    file.filename = filename
    if not upload_to_s3(file, code):
        return jsonify({"status": "error", "message": "Internal Server error"})
    return jsonify(
        {
            "status": "success",
            "message": "File was successfully uploaded",
            "code": code,
        }
    )


@app.route("/download", methods=["GET"])
def download():

    code = request.args.get("code")
    path = request.args.get("path")

    if not path:
        home = os.path.expanduser("~")
        path = os.path.join(home, "Downloads")

    
    if not code:
        return jsonify({"status": "failed", "message": "code is required"})

    code = int(code)
    if not valid_code(code):
        return jsonify({"status": "failed", "message": f"code {code} is not valid"})

    download_from_s3(code, path)

    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run()
