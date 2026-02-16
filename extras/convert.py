import os
import subprocess
from utils import *

def convert_video(input_file_path, output_file_path):
    try:
        # Adjust the ffmpeg command to save audio in WAV format with a sample rate of 16000 Hz
        run_subprocess(['ffmpeg', '-i', input_file_path, '-ar', '16000', '-ac', '1', '-f', 'wav', output_file_path])
        return True
    except subprocess.CalledProcessError as e:
        handle_conversion_error(input_file_path, e)
        return False

def get_output_file_path(video_file, output_folder):
    # Change the output file extension to '.wav'
    output_file = os.path.splitext(video_file)[0] + '.wav'
    return os.path.join(output_folder, output_file)

def convert_videos_in_folder(video_folder, output_folder):
    check_directory_exists(video_folder, 'video')
    check_directory_exists(output_folder, 'output')

    video_files = get_video_files(video_folder)

    for video_file in video_files:
        output_file_path = get_output_file_path(video_file, output_folder)
        if not os.path.exists(output_file_path):
            input_file_path = os.path.join(video_folder, video_file)
            if convert_video(input_file_path, output_file_path):
                print_success(f"Successfully converted {video_file} to {os.path.basename(output_file_path)} in {output_folder}\n")
        else:
            print_success(f"Skipped conversion: Converted file {os.path.basename(output_file_path)} already exists in {output_folder}.\n")
