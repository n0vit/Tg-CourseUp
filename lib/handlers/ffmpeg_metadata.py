from __future__ import unicode_literals
import math
import ffmpeg
import os
from pprint import pprint # for printing Python dictionaries in a human-readable way

# read the audio/video file from the command line arguments
# media_file = sys.argv[1]
# uses ffprobe command to extract all possible metadata from the media file
class VideoMeatadata:
    def get_video_metadata(path:str) -> list:
        try:
            probe = ffmpeg.probe(path)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            duration = round(float(video_stream['duration']))
            return[width,height,duration]
        
        except ffmpeg.Error as e:
            print('stdout:', e.stdout.decode('utf8'))
            print('stderr:', e.stderr.decode('utf8'))
       
        

# def read_frame_as_jpeg(in_filename, frame_num):
#     out, err = (
#         ffmpeg
#         .input(in_filename)
#         .filter('select', 'gte(n,{})'.format(frame_num))
#         .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
#         .run(capture_stdout=True)
#     )
#     with open(os.path.dirname(path)+'\\video.jpeg', 'wb') as f:
#         f.write(out)
#     return out


