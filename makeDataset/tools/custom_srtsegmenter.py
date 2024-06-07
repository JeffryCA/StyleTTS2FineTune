import glob
import os

import pysrt
from pydub import AudioSegment
from tqdm import tqdm

base = "."

output_dir = f"{base}/segmentedAudio/"  # path to where you want the segmented audio to go. dont touch this unless youre having issues
bad_audio_dir = f"{base}/badAudio/"  # path to where you want the bad audio to go. dont touch this unless youre having issues
srt_dir = f"{base}/processed/"
audio_dir = f"{base}/wav/"

os.makedirs(output_dir, exist_ok=True)
os.makedirs(bad_audio_dir, exist_ok=True)
os.makedirs(srt_dir, exist_ok=True)
os.makedirs(audio_dir, exist_ok=True)
os.makedirs(f"{base}/trainingdata", exist_ok=True)

srt_list = glob.glob(f"{srt_dir}*.srt")  # Gets a list of all srt files
# sort the list of srt files by name
srt_list.sort()
audio_list = glob.glob(f"{audio_dir}*.wav")  # Gets a list of all audio files


if len(srt_list) == 0 or len(audio_list) == 0:
    raise Exception(
        f"You need to have at least 1 srt file and 1 audio file, you have {len(srt_list)} srt and {len(audio_list)} audio files!"
    )


print(f"SRT Files: {len(srt_list)}")


for sub_file in tqdm(srt_list):  # Iterate over all srt files
    subs = pysrt.open(sub_file)
    audio_name = os.path.basename(sub_file).replace(".srt", ".wav")

    audio = AudioSegment.from_wav(f"./{audio_dir}/{audio_name}")
    with open(f"{base}/trainingdata/output.txt", "a+") as out_file:
        last_end_time = 0

    with open(f"{base}/trainingdata/output.txt", "a+") as out_file:

        for i, sub in enumerate(subs):
            # get start and end times in milliseconds
            start_time = (
                sub.start.minutes * 60 + sub.start.seconds
            ) * 1000 + sub.start.milliseconds
            end_time = (
                sub.end.minutes * 60 + sub.end.seconds
            ) * 1000 + sub.start.milliseconds

            audio_segment = audio[start_time:end_time]
            duration = len(audio_segment)
            filename = f"{audio_name[:-4]}_{i}.wav"

            # If the duration is within the desired range, then we keep, anything outside this range goes into the badAudio folder
            if 1850 <= duration <= 12000:  # Adjust these values to your desired range

                audio_segment.export(os.path.join(output_dir, filename), format="wav")
                out_file.write(f"{filename}|{sub.text}|1\n")
            else:
                bad_dir = os.path.join(
                    bad_audio_dir, "_".join(filename.split("_")[:-1])
                )
                os.makedirs(bad_dir, exist_ok=True)
                audio_segment.export(
                    os.path.join(bad_dir, f"{i}-{duration}.wav"),
                    format="wav",
                )
