
import threading
import numpy as np
import streamlit as st
from streamlit_webrtc import AudioProcessorBase, WebRtcMode, webrtc_streamer,VideoTransformerBase,ClientSettings
from PIL import Image
from aiortc.contrib.media import MediaRecorder
from neural_style_transfer import get_model_from_path, style_transfer


def webcam_input():
    st.header("Super_Resolution_Module")
    WIDTH = st.sidebar.select_slider('QUALITY (May reduce the speed)', list(range(150, 501, 50)))

    class NeuralStyleTransferTransformer(VideoTransformerBase):
        _width = WIDTH
        _model = None

        def __init__(self) -> None:
            self._model_lock = threading.Lock()

            self._width = WIDTH
            self._update_model()

        def set_width(self, width):
            update_needed = self._width != width
            self._width = width
            if update_needed:
                self._update_model()


        def _update_model(self):
            with self._model_lock:
                self._model = get_model_from_path()

        def transform(self, frame):
            image = frame.to_ndarray(format="bgr24")

            if self._model == None:
                return image

            orig_h, orig_w = image.shape[0:2]

            # cv2.resize used in a forked thread may cause memory leaks
            input = np.asarray(Image.fromarray(image).resize((self._width, int(self._width * orig_h / orig_w))))

            with self._model_lock:
                transferred = style_transfer(input, self._model)

            result = Image.fromarray((transferred * 255).astype(np.uint8))
            return np.asarray(result.resize((orig_w, orig_h)))

    ctx = webrtc_streamer(
        client_settings=ClientSettings(
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={"video": True, "audio": False},
        ),
        video_transformer_factory=NeuralStyleTransferTransformer,
        key="neural-style-transfer",
    )
    if ctx.video_transformer:
        ctx.video_transformer.set_width(WIDTH)



MEDIA_STREAM_CONSTRAINTS = {
    "video": False,
    "audio": {
        # these setting doesn't work
         "sampleRate": 16000,
        # "sampleSize": 16,
        # "channelCount": 1,
        "echoCancellation": False,  # don't turn on else it would reduce wav quality
        "noiseSuppression": True,
        "autoGainControl": True,
    },
}


def audio_input(wavpath):

    def recorder_factory():
        return MediaRecorder(wavpath)

    webrtc_ctx = webrtc_streamer(
        key="sendonly-audio",
        # mode=WebRtcMode.SENDONLY,
        mode=WebRtcMode.SENDRECV,
        in_recorder_factory=recorder_factory,
        media_stream_constraints=MEDIA_STREAM_CONSTRAINTS,
    )