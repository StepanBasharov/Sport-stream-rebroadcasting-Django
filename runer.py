import ffmpeg_streaming
from ffmpeg_streaming import Formats, Bitrate, Representation, Size
import sys
import argparse


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-in', '--input', default='none', action="store", required=True)
    parser.add_argument('-o', '--output', default='none', action="store", required=True)

    return parser


def run_ffmpeg():
    args = createParser()
    arg =args.parse_args()
    print(arg.input)
    video = ffmpeg_streaming.input(arg.input)

    _240p  = Representation(Size(426, 240), Bitrate(150 * 1024, 47 * 1024))
    _360p  = Representation(Size(640, 360), Bitrate(276 * 1024, 64 * 1024))
    _480p  = Representation(Size(854, 480), Bitrate(750 * 1024, 96 * 1024))
    hls = video.hls(Formats.h264())
    hls.representations(_240p, _360p, _480p)
    hls.output("mainsite/static/video/" + arg.output)

while True:
    try:
        run_ffmpeg()
    except Exception as e:
        with open("log.txt", "a+") as f:
            f.write(e + "\n")
        run_ffmpeg()
