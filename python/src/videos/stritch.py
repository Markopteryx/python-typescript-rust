import os
import subprocess

folder_name = 'downloaded_videos'
output_file_ts = 'combined_video.ts'
output_file_mp4 = 'combined_video.mp4'  # Output file name for the converted MP4 video

# Generate a list of video file paths in the directory
video_files = [os.path.join(folder_name, f) for f in sorted(os.listdir(folder_name)) if f.endswith('.ts')]

# Create a temporary file listing all video files
with open('file_list.txt', 'w') as list_file:
    for file in video_files:
        list_file.write(f"file '{file}'\n")

# Use ffmpeg to concatenate the video files
concat_command = f"ffmpeg -f concat -safe 0 -i file_list.txt -c copy {output_file_ts}"
subprocess.run(concat_command, shell=True)

# Convert the combined TS video to MP4
convert_command = f"ffmpeg -i {output_file_ts} -c copy {output_file_mp4}"
subprocess.run(convert_command, shell=True)

# Optionally, remove the temporary file list and the intermediate TS file
os.remove('file_list.txt')
os.remove(output_file_ts)

print(f"Combined video saved as {output_file_mp4}")