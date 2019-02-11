import ffmpeg
import os

def make_preview_image(in_filename, out_filename, time, width):
    ffmpeg.input(in_filename, ss=time).filter('scale', width, -1).output(out_filename, vframes=1).run()

def make_preview_image_crop_left_half(in_filename, out_filename, time, width):
    ffmpeg.input(in_filename, ss=time).filter_('crop', x = '0', y = '0', w = '1/2*in_w', h = 'in_h').filter('scale', width, -1).output(out_filename, vframes=1).run()

def make_preview_image_chromakey_image(in_video_filename, in_background_filename, time, color, out_filename, override_output_file = ""):
    os.system('ffmpeg -' + override_output_file + ' -i ' + in_background_filename + ' -i ' + in_video_filename + ' -ss ' + time + ' -q:v 2 -filter_complex "[1:v]chromakey=' + color + '[ckout];[0:v][ckout]overlay, transpose = 1[out]" -map "[out]" ' + out_filename)