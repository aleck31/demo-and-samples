from os import listdir
from os.path import isfile, join
from pathlib import Path
import boto3


DEMO_REGION = 'us-east-1'
# Alternative regions for different engine support:
# DEMO_REGION = 'eu-central-1'  # Supports: standard, neural, generative
# DEMO_REGION = 'us-west-2'     # Supports: standard, neural, generative
# DEMO_REGION = 'ap-southeast-1' # Supports: standard, neural only
# DEMO_REGION = 'cn-northwest-1' # Supports: standard only (China region)

AUDIO_OUTPUT = './audio_samples'

# All four engines (us-east-1 supports all engines)
ENGINES = ['standard', 'neural', 'generative', 'long-form']

# For other regions, comment out unsupported engines:
# China Region: ENGINES = ['standard']
# Most regions: ENGINES = ['standard', 'neural']
# us-east-1, eu-central-1, us-west-2: ENGINES = ['standard', 'neural', 'generative']
# Only us-east-1: ENGINES = ['standard', 'neural', 'generative', 'long-form']


def print_engine_info():
    """Print information about the engines being used"""
    print("🎙️  Amazon Polly TTS Engine Information:")
    print("=" * 50)
    
    engine_info = {
        'standard': '📢 Standard: Traditional TTS, lowest cost',
        'neural': '🧠 Neural: More natural voices, moderate cost',
        'generative': '🤖 Generative: Most human-like, conversational (Higher cost)',
        'long-form': '📚 Long-form: Optimized for long content, premium quality (Highest cost)'
    }
    
    for engine in ENGINES:
        if engine in engine_info:
            print(f"  {engine_info[engine]}")
    
    # Cost warning for premium engines
    premium_engines = [e for e in ENGINES if e in ['generative', 'long-form']]
    if premium_engines:
        print("\n⚠️  WARNING: Premium engines have significantly higher costs!")
        print(f"   Premium engines in use: {', '.join(premium_engines)}")
        print("   Check AWS Polly pricing: https://aws.amazon.com/polly/pricing/")
    
    print(f"\n🌍 Region: {DEMO_REGION}")
    print(f"📁 Output directory: {AUDIO_OUTPUT}")
    print("=" * 50)


def ensure_required_path(inputs):
    required_path = inputs['audio_dest']    
    for engine in ENGINES:
        Path(f"{required_path}/{engine}").mkdir(parents=True, exist_ok=True)

def define_data(client, inputs, engine, data):
    data[engine] = {}
    lang_path = inputs['languages_path']
    lang = [f for f in listdir(lang_path) if isfile(join(lang_path, f))]

    larr = []
    [larr.append(l.replace(inputs['languages_file_ext'], '')) for l in lang]

    voices = client.describe_voices()
    for voice in larr:
        for vdata in voices['Voices']:
            if engine in vdata['SupportedEngines'] and voice in vdata['LanguageName']:

                vd = data[engine].get(voice)
                if vd:
                    vd.append({
                        'LanguageCode': vdata['LanguageCode'],
                        'VoiceId': vdata['Id']
                    })
                else:
                    data[engine][voice] = [{
                        'LanguageCode': vdata['LanguageCode'],
                        'VoiceId': vdata['Id']
                    }]


def synthesize_speech_mp3(client, inputs):
    kwargs = inputs['kwargs']
    response = client.synthesize_speech(**kwargs)

    file_path = inputs['mp3_file_path']
    file = open(file_path, 'wb')
    file.write(response['AudioStream'].read())
    file.close()


def read_file_to_xml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
        file.close()

    return f'<speak>\n\t{data}\n</speak>'


def run(client, inputs):
    data = {}

    for engine in inputs['engines']:

        if inputs['gen_data']:
            define_data(client, inputs, engine, data)

    for engine in inputs['engines']:

        count = 0
        for lan in data[engine]:
            for voice in data[engine][lan]:
                path_in = f'{inputs["languages_path"]}/{lan}.txt'
                text = read_file_to_xml(path_in)
                path = f'{inputs["audio_dest"]}/{engine}/{lan}-{voice["LanguageCode"]}-{voice["VoiceId"]}.{inputs["OutputFormat"]}'
                print(f'synthesizing: {path}')
                synthesize_speech_mp3(client, {
                    'mp3_file_path': path,
                    'kwargs': {
                        'VoiceId': voice["VoiceId"],
                        'LanguageCode': voice["LanguageCode"],
                        'OutputFormat': inputs["OutputFormat"],
                        'Text': text,
                        'TextType': inputs['TextType'],
                        'Engine': engine,
                    }
                })
                count += 1

        print(f'\nsynthesized {count} audio files for engine: {engine}\n\n')


if __name__ == "__main__":
    # Print engine information before starting
    print_engine_info()
    
    inputs = {
        'gen_data': True,
        'languages_file_ext': '.txt',
        'data_file_path': './data.py',
        'languages_path': './languages',
        'engine': 'standard',
        'engines': ENGINES,
        'audio_dest': AUDIO_OUTPUT,
        'OutputFormat': 'mp3',
        'TextType': 'ssml'
    }

    client = boto3.Session(region_name=DEMO_REGION).client('polly')
    ensure_required_path(inputs)
    run(client, inputs)
