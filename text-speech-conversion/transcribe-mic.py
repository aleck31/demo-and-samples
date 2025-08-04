# This example uses the sounddevice library to get an audio stream from the microphone. 
# The dependency of the project can be installed with pip:
# `pip install amazon-transcribe sounddevice`
import asyncio
import os
import sounddevice
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent


# Setup up demo region
DEMO_REGION = 'cn-northwest-1'
# DEMO_REGION = 'us-east-1'
# language code value set: zh-CN, zh-HK, en-US, en-GB, ar-AE, ar-SA, fi-FI, pl-PL, no-NO, nl-NL, pt-PT, 
# es-ES, th-TH, de-DE, it-IT, fr-FR, ko-KR, hi-IN, en-AU, sv-SE, pt-BR, ja-JP, ca-ES, es-US, fr-CA, 
SOURCE_LANGCODE = 'zh-CN'

# Be sure to use the correct parameters for the audio stream that matches
# the audio formats described for the source language you'll be using:
# https://docs.aws.amazon.com/transcribe/latest/dg/streaming.html
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024 * 4

CHANNEL_NUMS = 1
AUDIO_PATH = 'output-audio/test.mp3'
BYTES_PER_SAMPLE = 2


"""
Here's an example of a custom event handler you can extend to process
the returned transcription results as needed. 
This handler will simply print the text out to your interpreter.
"""
class MyEventHandler(TranscriptResultStreamHandler):
    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        # This handler can be implemented to handle transcriptions as needed.        
        results = transcript_event.transcript.results
        for result in results:
            if result.is_partial:
                for alt in result.alternatives:
                    #'​clear​' for Linux&Mac
                    os.system('cls')
                    print(alt.transcript)
            else:
                # add a mark for each segment end
                print('🔚')



async def mic_stream():
    # This function wraps the raw input stream from the microphone forwarding
    # the blocks to an asyncio.Queue.
    loop = asyncio.get_event_loop()
    input_queue = asyncio.Queue()

    def callback(indata, frame_count, time_info, status):
        loop.call_soon_threadsafe(input_queue.put_nowait, (bytes(indata), status))

    stream = sounddevice.RawInputStream(
        channels=CHANNEL_NUMS,
        samplerate=SAMPLE_RATE,
        blocksize=CHUNK_SIZE,
        callback=callback,
        dtype="int16",
    )
    # Initiate the audio stream and asynchronously yield the audio chunks
    # as they become available.
    with stream:
        while True:
            indata, status = await input_queue.get()
            yield indata, status


async def write_chunks(stream):
    # This connects the raw audio chunks generator coming from the microphone
    # and passes them along to the transcription stream.
    async for chunk, status in mic_stream():
        await stream.input_stream.send_audio_event(audio_chunk=chunk)
    await stream.input_stream.end_stream()


async def basic_transcribe():
    client = TranscribeStreamingClient(region=DEMO_REGION)

    # Start transcription to generate async stream
    stream = await client.start_stream_transcription(
        language_code=SOURCE_LANGCODE,
        media_sample_rate_hz=SAMPLE_RATE,
        media_encoding="pcm"
    )

    # Instantiate our handler and start processing events
    handler = MyEventHandler(stream.output_stream)
    await asyncio.gather(write_chunks(stream), handler.handle_events())


loop = asyncio.get_event_loop()
loop.run_until_complete(basic_transcribe())
loop.close()
