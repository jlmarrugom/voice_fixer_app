from voicefixer.base import VoiceFixer
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from io import BytesIO
import soundfile as sf

st.set_page_config(page_title="VoiceFixer app", page_icon=":notes:")
st.title("Voice Fixer App :notes:")
st.write(
    """
    This app is a mix of [VoiceFixer Model](https://github.com/haoheliu/voicefixer), and a custom
    Streamlit component that [records audio](https://github.com/Joooohan/audio-recorder-streamlit) Online.
    Currently the app shows great results when removing background noises, but 
    speech improvements aren't as obvious.
    """)
#Config files are on voicefixer/base and voicefixer/vocoder/config import
# They were uploaded on hugging face
voicefixer = VoiceFixer()
audio_bytes = audio_recorder(
    pause_threshold= 1.5
)
try:
    data, samplerate = sf.read(BytesIO(audio_bytes))
    print(samplerate)
    sf.write("original.wav",data,samplerate)
    st.audio(audio_bytes, format = "audio/wav")
    if data.shape[0]>=10000:
        voicefixer.restore(input="original.wav", # low quality .wav/.flac file
                       output="enhanced_output.wav",
                       cuda=False, # GPU acceleration
                       mode=0)
        st.write("The Audio without background noises and a little enhancement :ocean:")
        st.audio("enhanced_output.wav")

    else: st.warning("Recorded Audio is too short, try again :relieved:")#wink
except:
    st.info("Try to record some audio :relieved:")