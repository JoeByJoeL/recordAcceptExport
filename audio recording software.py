import keyboard
import numpy as np
import os
import sounddevice as sd
import soundfile as sf
import time

recorded_audio = []
first_time = True

threshold = 1000

while True:
    if first_time:
        time.sleep(0.2)
        os.system("cls")
        first_time = False
        print("Recording. Press s to stop.")
        audio_data = sd.rec(60 * 44100, 44100, 2, 'int16')

    if keyboard.is_pressed('s'):
        first_time = True
        print("Stopped. Playing back.")
        sf.write('recorded_audio.wav', audio_data, 44100)
        
        non_silent_indices = np.where(np.abs(audio_data[:, 0]) > threshold)[0]
        if len(non_silent_indices) > 0:
            start_index = non_silent_indices[0]
            end_index = non_silent_indices[-1]
            trimmed_audio = audio_data[start_index:end_index + 1, :]
        else:
            trimmed_audio = np.array([])

        sf.write('trimmed_recorded_audio.wav', trimmed_audio, 44100)
        sd.play(trimmed_audio, 44100)
        
        print("A-Discard")
        print("D-Accept")
        print("W-Accept and Export")

        while True:
            if keyboard.is_pressed('a'):
                print("Discarded.")
                break
            elif keyboard.is_pressed('d'):
                recorded_audio.append(trimmed_audio)
                print("Accepted.")
                break
            elif keyboard.is_pressed('w'):
                recorded_audio.append(trimmed_audio)
                print("Accepted.")
                concatenated_audio = np.concatenate(recorded_audio, axis=0)
                sf.write('recorded_audio.wav', concatenated_audio, 44100)
                os.remove('trimmed_recorded_audio.wav')
                print("Exported.")
                time.sleep(1)
                exit()