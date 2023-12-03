import os
import random
import shutil
import subprocess

def get_video_duration_ffmpeg(video_path):
    try:
        ffprobe_path = subprocess.check_output(['brew', '--prefix', 'ffmpeg']).decode('utf-8').strip() + '/bin/ffprobe'
        command = [ffprobe_path, '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_path]
        duration = float(subprocess.check_output(command))
        return duration
    except Exception as e:
        print(f"Error: {e}")
        return None

def move_random_videos(input_folder, output_folder, target_duration):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all subdirectories in the input folder
    subdirectories = sorted([f.path for f in os.scandir(input_folder) if f.is_dir()])

    total_duration = 0
    i = 1  # Serial number for the moved videos

    # Loop through subdirectories
    #print(f"{subdirectories}")
    while total_duration < target_duration:
        for subdir in subdirectories:
            video_files = [f.path for f in os.scandir(subdir) if f.is_file() and f.name.endswith(('.mp4', '.avi', '.mkv', '.mov'))]

            random.shuffle(video_files)
            video_file = random.choice(video_files)
            clip_duration = get_video_duration_ffmpeg(video_file)
            if total_duration <= target_duration:
                total_duration += clip_duration
                # Customize the naming here (e.g., add a custom prefix and suffix)
                new_filename = f"{i}_{os.path.basename(video_file)}"
                i += 1  # Increment serial number for the next video
                output_path = os.path.join(output_folder, new_filename)
                shutil.move(video_file, output_path)
                print(new_filename)
            else:
                # If adding the current clip exceeds the target duration, break the loop
                print("Target duration reached. Stopping.")
                print(total_duration)
                break

    print("Processing complete.")

if __name__ == "__main__":
    input_folder = "/Users/shahoreertalha/Desktop/learn/clips"
    output_folder = "/Users/shahoreertalha/Desktop/learn/clips_output"
    target_duration = float(input("Enter the target duration for the output video (in seconds): "))

    move_random_videos(input_folder, output_folder, target_duration)