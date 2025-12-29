#Convert videos to mp3 format
import os, subprocess

files = os.listdir('videos')
for file in files:
    video_no = file.split(' [')[0].split(" #")[1]
    file_name = file.split('｜')[0]
    print(file_name, video_no)

    subprocess.run(['ffmpeg', '-i', f'videos/{file}', f'audios/{video_no}_{file_name}.mp3'])
    print(f'Converted {file} to mp3 format.')