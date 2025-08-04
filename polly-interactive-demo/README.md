# Amazon Polly TTS (Text to Speech) Interactive Demo

This project harnesses Amazon Polly text-to-speech service, featuring an interactive demo:
- Real-time voice synthesis with customizable text and instant playback
- 40+ languages including Chinese (Mandarin and Cantonese)
- 100+ voice options

### Prerequisites
- AWS Account with sufficient [AWS Identity and Access Management (IAM)](https://aws.amazon.com/iam/) permissions.
- [Python 3.10](https://www.python.org/downloads/) or later and
  [pip package installer](https://pip.pypa.io/en/stable/), to package Python code for Lambda.
- Install python dependencies
    - `pip install -r ./requirements.txt`
- Activate virtual environment (if using one):
    - `source .venv/bin/activate`

### Quick Start

Run the interactive demo script to test individual voices with sample or custom text:

```shell
$ python ./polly_demo.py
```

The interactive demo allows you to:
- 🎛️ Select voice engine (neural, standard, generative, long-form)
- 🌍 Choose from available languages and voices
- 📝 Input custom text or use sample text from the `languages` directory
- 🔊 Generate and play speech in real-time

## License

This project is licensed under the Apache-2.0 License.
