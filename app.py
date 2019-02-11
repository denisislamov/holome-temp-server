#!flask/bin/python
import json
import os.path
import time
import ffmpeg_helpers

from flask import Flask

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
    file_infos = []
    directory = os.getcwd() + "/data"
    for file in os.listdir(directory):
        file_info = FileInfo(file, time.ctime(os.path.getmtime(directory + "/" + file)),
                             time.ctime(os.path.getctime(directory + "/" + file)))
        file_infos.append(file_info)

    return json.dumps(file_infos, cls=FileInfoEncoder)


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


@app.route('/holome/api/v1.0/getallinfo', methods=['GET'])
def get_all_info():
    return get_all_files_info()


@app.route('/holome/api/v1.0/makepreviewimage/<string:infilename>/<string:outfilename>/<string:time>/<string:width>',
           methods=['GET'])
def get_make_preview_image(infilename, outfilename, time, width):
    ffmpeg_helpers.make_preview_image(infilename, outfilename, time, width)


@app.route(
    '/holome/api/v1.0/makepreviewimagecroplefthalf/<string:infilename>/<string:outfilename>/<string:time>/<string:width>',
    methods=['GET'])
def get_make_preview_image_crop_left_half(infilename, outfilename, time, width):
    ffmpeg_helpers.make_preview_image_crop_left_half(infilename, outfilename, time, width)


@app.route(
    '/holome/api/v1.0/makepreviewimagechromakeyimage/<string:infilename>/<string:outfilename>/<string:time>/<string:width>',
    methods=['GET'])
def get_make_preview_image_chromakey_image(invideofilename, inbackgroundfilename, time, color, outfilename,
                                           overrideoutputfile):
    ffmpeg_helpers.make_preview_image_chromakey_image(invideofilename, inbackgroundfilename, time, color, outfilename,
                                                      overrideoutputfile)


if __name__ == '__main__':
    app.run(debug=True)
