import os
import asyncio
import sounddevice
from pydub.playback import play
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent
from amazon_transcribe.client import TranscribeStreamingClient
from modules.polly import polly_read
from modules.translate import translate_txt


# Setup up demo region
DEMO_REGION = 'us-east-1'
# DEMO_REGION = 'cn-northwest-1'

# language code value set: zh-CN, zh-HK, en-US, en-GB, ar-AE, ar-SA, fi-FI, pl-PL, no-NO, nl-NL, pt-PT, 
# es-ES, th-TH, de-DE, it-IT, fr-FR, ko-KR, hi-IN, en-AU, sv-SE, pt-BR, ja-JP, ca-ES, es-US, fr-CA, 
SOURCE_LANGCODE = 'zh-CN'
TARGET_LANGCODE = 'en-US'

# Be sure to use the correct parameters for the audio stream that matches
# the audio formats described for the source language you'll be using:
# https://docs.aws.amazon.com/transcribe/latest/dg/streaming.html
SAMPLE_RATE = 16000
READ_CHUNK = 1024
CHUNK_SIZE = 1024 * 4
BYTES_PER_SAMPLE = 2
CHANNEL_NUMS = 1
# AUDIO_PATH = 'output-audio/test.mp3'


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
                first_lang_text = result.alternatives[0].transcript
                second_lang_text = translate_txt(DEMO_REGION, first_lang_text, SOURCE_LANGCODE, TARGET_LANGCODE)
                sound = polly_read(DEMO_REGION, second_lang_text)
                # Need ffmpeg to support mp3 format
                play(sound)


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


async def transcribe_n_translate():
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


def main():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(transcribe_n_translate())
    loop.close()

if __name__ == '__main__':
    main()