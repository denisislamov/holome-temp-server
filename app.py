#!flask/bin/python
from flask import Flask, jsonify
import os.path, time
import json

app = Flask(__name__)


class FileInfo(object):
    def __init__(self, filename, last_modified_date, created_date):
        self.filename = filename
        self.last_modified_date = last_modified_date
        self.created_date = created_date


class FileInfoEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, FileInfo):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


def get_all_files_info():
    fileInfos = []
    directory = os.getcwd() + "/data"
    for file in os.listdir(directory):
        fileInfo = FileInfo(file, time.ctime(os.path.getmtime(directory + "/" + file)),
                            time.ctime(os.path.getctime(directory + "/" + file)))
        fileInfos.append(fileInfo)

    return json.dumps(fileInfos, cls=FileInfoEncoder)


def creation_date(file):
    return "last modified: %s" % time.ctime(os.path.getmtime(file)) + "\n" + "created: %s" % time.ctime(
        os.path.getctime(file))


def get_all_files(extension):
    result = ""

    for file in os.listdir(os.getcwd() + "/data"):
        if file.endswith("." + extension):
            result += file + "\n"

    return result


@app.route('/holome/api/v1.0/getmp4', methods=['GET'])
def get_all_mp4_files():
    return get_all_files("mp4")


@app.route('/holome/api/v1.0/getjpg', methods=['GET'])
def get_all_jpg_files():
    return get_all_files("jpg")


@app.route('/holome/api/v1.0/getpng', methods=['GET'])
def get_all_jpg_files():
    return get_all_files("png")


@app.route('/holome/api/v1.0/getcreationdate/<string:filename>', methods=['GET'])
def get_creation_date(filename):
    return creation_date(os.getcwd() + "/data/" + filename)


@app.route('/holome/api/v1.0/getallinfo', methods=['GET'])
def get_all_info():
    return get_all_files_info()


if __name__ == '__main__':
    app.run(debug=True)
