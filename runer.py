import ffmpeg_streaming
from ffmpeg_streaming import Formats, Bitrate, Representation, Size
import sys
import argparse
import subprocess


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-in', '--input', default='none', action="store", required=True)
    parser.add_argument('-o', '--output', default='none', action="store", required=True)

    return parser


def run_ffmpeg():
    args = createParser()
    arg =args.parse_args()
    print(arg.input)
    try:
        subprocess.check_output(['ffmpeg', '-re', '-i', arg.input, '-c', 'copy', '-f', 'flv', '-y', f'rtmp://{arg.output}'])
    except subprocess.CalledProcessError as e:
        print("fuck")
        test()

while True:
    try:
        run_ffmpeg()
    except Exception as e:
        with open("log.txt", "a+") as f:
            f.write(e + "\n")
        run_ffmpeg()
