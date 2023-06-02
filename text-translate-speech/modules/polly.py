#!/usr/bin/env python3
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
from tempfile import gettempdir
from pydub import AudioSegment
from pydub.playback import play



TEST_TXT="Amazon Polly 使用深度学习技术来合成听起来自然的人类语音，让您可以将文章转换为语音。"

def polly_play(region, input_text): 

    client = boto3.client('polly', region_name=region)

    try:
        response = client.synthesize_speech(
            Text=input_text, 
            # Support format: mp3, pcm, ogg_vorbis, json
            OutputFormat='mp3',
            # VoiceId='Zhiyu',
            VoiceId='Joanna',
            # Engine='standard'
            Engine='neural'
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
        sound = AudioSegment.from_file(output, 'mp3')
        # return sound
        # Need ffmpeg to support mp3 format
        print('📢')
        play(sound)

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)
