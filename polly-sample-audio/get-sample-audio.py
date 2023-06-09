from os import listdir
from os.path import isfile, join
from pathlib import Path
import boto3


DEMO_REGION = 'ap-southeast-1'
# DEMO_REGION = 'cn-northwest-1'
AUDIO_OUTPUT = './samples/'
ENGINES = ['standard', 'neural']
# neural not supported in China Region
# ENGINES = ['standard']


def ensure_required_path(inputs):
    required_path = inputs['audio_dest']    
    for engine in ENGINES:
        Path(required_path+engine).mkdir(parents=True, exist_ok=True)

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
