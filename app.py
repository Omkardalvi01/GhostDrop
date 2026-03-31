from flask import Flask, Response, jsonify, request, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import tempfile
import zipfile
import shutil
from file_storage import download_from_s3, upload_to_s3, s3_client
from utils import allowed_file, valid_code, make_code

app = Flask(__name__)
CORS(app)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1000 * 1000  # MAX Limit of file 5 MB


@app.route("/upload", methods=["POST"])
def upload():
    code = make_code()
    
    # Try fetching as single or multiple using getlist
    files = request.files.getlist("file") or request.files.getlist("files") or request.files.getlist("files[]")

    if not files:
        return jsonify({"status": "error", "message": "No file was selected"})
    
    # filter out empty filename
    actual_files = [f for f in files if f.filename != "" and f.filename is not None]
    if not actual_files:
        return jsonify({"status": "error", "message": "No file was selected"})

    uploaded_files = []
    
    for file in actual_files:
        filename = secure_filename(file.filename) # type: ignore
        if not allowed_file(filename):
            return jsonify(
                {
                    "status": "error",
                    "message": f"Supported format for now are .txt, .pdf, .png, .jpg, .jpeg, .gif. File '{filename}' not allowed.",
                },
            )

        file.filename = filename # type: ignore
        if not upload_to_s3(file, code):
            return jsonify({"status": "error", "message": f"Internal Server error uploading {filename}"})
        
        uploaded_files.append(filename)

    return jsonify(
        {
            "status": "success",
            "message": f"{len(uploaded_files)} file(s) successfully uploaded",
            "code": code,
        }
    )


@app.route("/download", methods=["GET"])
def download():
    code = request.args.get("code")
    
    if not code:
        return jsonify({"status": "failed", "message": "code is required"})

    code_int = int(code)
    if not valid_code(code_int):
        return jsonify({"status": "failed", "message": f"code {code} is not valid"})

    str_code = str(code_int)
    responses = s3_client.list_objects_v2(Bucket="ghostdrop", Prefix=f"{str_code}/")
    
    files_data = []
    for obj in responses.get("Contents", []):
        filename = obj['Key'][len(str_code)+1:]
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": "ghostdrop",
                "Key": obj["Key"],
                "ResponseContentDisposition": f'attachment; filename="{filename}"'
            },
            ExpiresIn=3600
        )
        files_data.append({"filename": filename, "url": url})
        
    if not files_data:
        return jsonify({"status": "failed", "message": "No files found for this code."})

    return jsonify({"status": "success", "files": files_data})


if __name__ == "__main__":
    app.run()
