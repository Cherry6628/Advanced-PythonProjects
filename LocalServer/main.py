print("Started Imports...", end="", flush=True)
from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO
import os
import uuid
from time import sleep
print("\rAll Modules Imported!", end="", flush=True)
sleep(1), print("\rUploaded Files : \r")

app = Flask(__name__)
socketio = SocketIO(app)

uploaded_files = []


def fileSize_STR(size):
    size = int(size)
    dict_ = {
        "YB": 0,
        "ZB": 0,
        "EB": 0,
        "PB": 0,
        "TB": 0,
        "GB": 0,
        "MB": 0,
        "KB": 0,
        "B": 0
    }
    order = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    unit_sizes = [1, 1024, 1024**2, 1024**3, 1024**4, 1024**5, 1024**6, 1024**7, 1024**8]

    for i in range(len(order) - 1, -1, -1):
        if size >= unit_sizes[i]:
            dict_[order[i]] = size // unit_sizes[i]
            size %= unit_sizes[i]

    return "  ".join(f"{y:>3}{x}" for x, y in dict_.items() if y != 0)


@app.route('/')
def index():
    return render_template('index.html', files=uploaded_files)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    if filename in uploaded_files:  # Prevents Other Data from being downloaded or shown.
        return send_from_directory(UPLOAD_FOLDER, filename)
    return "Forbidden", 403


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    file.stream.seek(0, os.SEEK_END)
    size = file.stream.tell()
    file.stream.seek(0)
    if size > Max_bytes:
        return "Payload Too Large", 413
    else:
        filename = file.filename

        file.save(os.path.join(UPLOAD_FOLDER, filename))

        file_name_to_show = filename if len(filename) < 50 else filename[:47]+'...'
        print(f"{file_name_to_show:50} - {fileSize_STR(size)}")

        uploaded_files.append(filename)
        socketio.emit('new_file', {'filename': filename})

        return "File uploaded", 200


if __name__ == '__main__':
    Max_bytes = 10 * (1024 ** 3)  # Maximum Bytes per Single File

    UPLOAD_FOLDER = 'uploads'
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    host_ip, port = "192.168.1.35", 5000

    socketio.run(app, host=host_ip, port=port, debug=False, allow_unsafe_werkzeug=True)
