import streamlit as st

from input import  audio_input, webcam_input
import sounddevice as sd
import tempfile
import glob
import os
from scipy.io.wavfile import write
import time
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, ClientSettings
from output import play_audio
import subprocess
import numpy as np
from pathlib import Path

from aiortc.contrib.media import MediaRecorder


st.title("VidCon")
st.sidebar.title('Navigation')
method = st.sidebar.radio('Go To ->', options=['Super Resolution', 'Audio Denoising','Wav2Lip'])
st.sidebar.header('Options')



if method == 'Super Resolution':
    webcam_input()
elif method == 'Audio Denoising':

    st.markdown('# recorder')
    if "wavpath" not in st.session_state:
        cur_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
        tmp_wavpath = os.path.join("noisy_audio",f'{cur_time}.wav')
        st.session_state["wavpath"] = str(tmp_wavpath)

    wavpath = st.session_state["wavpath"]
    audio_input(wavpath)  # first way
    if Path(wavpath).exists():
        subprocess.run(f"python3 downsample.py {wavpath}",shell=True)
        subprocess.run(f"python3 -m denoiser.enhance --noisy_dir noisy_audio --out_dir clean_audio/",shell=True)
        clean_output_1 = glob.glob("clean_audio/*")[0]
        st.write(clean_output_1)
        play_audio(clean_output_1)

        clean_output_2 = glob.glob("clean_audio/*")[-1]
        st.write(clean_output_2)
        play_audio(clean_output_2)

    #if st.button('Denoise'):
    #    subprocess.run("python3 -m denoiser.enhance --noisy_dir noisy/ --out_dir clean/",shell=True)
    #if st.button('Play'):
    #    play_audio()
else:
    # def capture_video():
    #     def out_recorder_factory() -> MediaRecorder:
    #         return MediaRecorder("output.mp4", format="mp4")

    #     webrtc_streamer(key="sample",
    #         media_stream_constraints={
    #         "video": True,
    #         "audio": False,
    #         },
    #         out_recorder_factory=out_recorder_factory)

    #     if st.button('Stop'):
    #         return()
    
   
    def out_recorder_factory_video() -> MediaRecorder:
        return MediaRecorder("output.mp4", format="mp4")

    ctx = webrtc_streamer(key="video",
        client_settings=ClientSettings(
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={"video": True, "audio": False},
        ))

    def out_recorder_factory_audio() -> MediaRecorder:
        return MediaRecorder("output.wav", format="wav")

    webrtc_streamer(key="audio",
        client_settings=ClientSettings(
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={"video": False, "audio": True},
        ))

    if st.button("Show video"):
        video_file = open('output.mp4', 'rb')
        video_bytes = video_file.read()

        st.video(video_bytes)



    # if st.button('Record audio'):
    #     capture_audio()
    if st.button('Play audio'):
        play_audio()
