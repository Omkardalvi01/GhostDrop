from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from file_storage import download_from_s3, upload_to_s3, s3_client
from utils import allowed_file, valid_code, make_code, NamedBytes
from logs import add_to_logs, get_metadata

app = Flask(__name__)
CORS(app)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # MAX Limit of file 5 MB
# Manual limit of 10 files


@app.route("/upload", methods=["POST"])
def upload():
    str_file = None
    message = request.form.get("message", "")
    if message:
        str_file = NamedBytes(message.encode("utf-8"), "message.txt")

    files = (
        request.files.getlist("file")
        or request.files.getlist("files")
        or request.files.getlist("files[]")
    )
    files = files[:10]

    if not files and not str_file:
        return jsonify({"status": "error", "message": "No file was selected"})

    actual_files = [f for f in files if f.filename != "" and f.filename is not None]
    if not actual_files and not str_file:
        return jsonify({"status": "error", "message": "No file was selected"})

    code = make_code()
    uploaded_files = []
    sz = 0

    for file in actual_files:
        filename = secure_filename(file.filename)  # type: ignore
        if not allowed_file(filename):
            continue

        file.seek(0, 2)
        sz += file.tell()
        file.seek(0)

        file.filename = filename  # type: ignore
        if not upload_to_s3(file, code):
            return jsonify(
                {
                    "status": "error",
                    "message": f"Internal Server error uploading {filename}",
                }
            )

        uploaded_files.append(filename)

    if str_file:
        upload_to_s3(str_file, code)

    add_to_logs(request.remote_addr, code, len(actual_files), sz)

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
        filename = obj["Key"][len(str_code) + 1 :]
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": "ghostdrop",
                "Key": obj["Key"],
                "ResponseContentDisposition": f'attachment; filename="{filename}"',
            },
            ExpiresIn=3600,
        )
        files_data.append({"filename": filename, "url": url})

    if not files_data:
        return jsonify({"status": "failed", "message": "No files found for this code."})

    return jsonify({"status": "success", "files": files_data})


@app.route("/metadata", methods=["GET"])
def get_data():
    files_transfer, data_transfer = get_metadata()
    data_transfer = data_transfer * (10**-6)
    return jsonify(
        {"status": "success", "files": files_transfer, "data(Mb)": data_transfer}
    )


if __name__ == "__main__":
    app.run()
