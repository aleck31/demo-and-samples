# The dependency of the project can be installed with pip:
# `pip install pydub`
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
from tempfile import gettempdir
from pydub import AudioSegment
from pydub.playback import play


# Setup up demo region
DEMO_REGION = 'cn-northwest-1'
READ_CHUNK = 1024

REPLYTXT="Amazon Polly 使用深度学习技术来合成听起来自然的人类语音，让您可以将文章转换为语音。"


polly = boto3.client('polly', region_name=DEMO_REGION)

try:
    response = polly.synthesize_speech(
        Text=REPLYTXT, 
        # Support format: mp3, pcm, ogg_vorbis, json
        OutputFormat='mp3',
        VoiceId='Zhiyu',
        Engine='standard'
        # Engine='neural'
    )
except (BotoCoreError, ClientError) as error:
    print(error)
    sys.exit(-1)

# Access the audio stream from the response
if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = os.path.join(gettempdir(), "polly-speech.mp3")
            try:
            # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
            # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)
else:
    # The response didn't contain audio data, exit gracefully
    print("Could not stream audio")
    sys.exit(-1)


sound = AudioSegment.from_file(output, 'mp3')

'''
# pyaudio playback is not recommended
pa = pyaudio.PyAudio()
op_stream = pa.open(format = pa.get_format_from_width(sound.sample_width),
    channels = sound.channels,
    rate = sound.frame_rate,
    output = True)

data = sound.readframes(READ_CHUNK)

while data != '':
    op_stream.write(data)
    data = sound.readframes(READ_CHUNK)

op_stream.close()
pa.terminate()
'''

# Need ffmpeg to support mp3 format
# pip install ffmpeg-downloader
# ffdl install --add-path
play(sound)
