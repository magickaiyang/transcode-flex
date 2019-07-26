import re
import subprocess
from pathlib import Path
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Flexible Transcoding from x264 to x265')
    parser.add_argument('path', help='Path to the directory containing videos', type=str)
    args = parser.parse_args()

    base_cmd_1 = ['ffmpeg', '-hide_banner', '-loglevel', 'verbose', '-hwaccel', 'cuvid', '-c:v', 'h264_cuvid', '-i']
    base_cmd_2 = ['-c:v', 'hevc_nvenc', '-preset', 'slow', '-profile:v', 'main', '-tier', 'high', '-rc', 'vbr_hq',
                  '-rc-lookahead', '40', '-b:v', '3M', '-c:a', 'copy', '-c:s', 'copy']

    path = Path(args.path)
    videos = path.glob('**/*.mkv')
    for video in videos:
        video = str(video)
        output_video = video
        output_video = re.sub(r'\.mkv$', '', output_video, flags=re.IGNORECASE)  # removes suffix
        # removes references to x264 in filenames
        output_video = re.sub(r'\.H\.264-?', '', output_video, flags=re.IGNORECASE)
        output_video = re.sub(r'\.AVC-?', '', output_video, flags=re.IGNORECASE)
        output_video = re.sub(r'\.x264-?', '', output_video, flags=re.IGNORECASE)

        video = [video]
        output_video = [output_video + '.x265.mkv']
        cmd = base_cmd_1 + video + base_cmd_2 + output_video
        print(cmd)
        subprocess.run(cmd, check=True)
