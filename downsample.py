import librosa
import soundfile
import sys
from pydub.generators import WhiteNoise
from pydub import AudioSegment as am
import numpy as np
# total arguments
filepath = sys.argv[1]


import librosa    
y, s = librosa.load(filepath)

STD_n= 0.1
noise=np.random.normal(0, STD_n, y.shape[0])

y = y+noise


print("HELLO_ls")

y = librosa.resample(y,s,16000)
soundfile.write(filepath,y,16000)



"""

sound = am.from_file(filepath, format='wav', frame_rate=48000)

noise = WhiteNoise().to_audio_segment(duration=len(sound))
combined = sound.overlay(noise)


combined = combined.set_frame_rate(16000)

combined.export(filepath, format='wav', parameters=["-ac", "1"])
"""