# Text-Speech Conversion Tools

This project provides bidirectional conversion tools between text and speech using Amazon Transcribe and Amazon Polly services.

## 🔧 Tools Overview

### 🔊 **polly-play.py** - Text-to-Speech  
- Text-to-speech synthesis using Amazon Polly
- Converts predefined text into spoken audio
- Generates MP3 audio files and plays them
- Uses Chinese voice 'Zhiyu' with Standard engine

### 🎤 **transcribe-mic.py** - Speech-to-Text
- Real-time microphone transcription using Amazon Transcribe
- Converts spoken words into text
- Supports multiple languages (currently configured for Chinese zh-CN)
- Live display of transcription results

## Prerequisites

- AWS Account with sufficient [IAM permissions](https://aws.amazon.com/iam/)
- [Python 3.10+](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/)
- Microphone access for speech recognition
- Audio output device for speech playback

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# For MP3 playback support, install ffmpeg
pip install ffmpeg-downloader
ffdl install --add-path
```

## Usage

### Speech Synthesis (Text → Speech)
```bash
python polly-play.py
```
- Converts predefined Chinese text to speech
- Plays the generated audio automatically

### Speech Recognition (Speech → Text)
```bash
python transcribe-mic.py
```
- Speak into your microphone
- See real-time transcription on screen
- Press Ctrl+C to stop

## Configuration

### Region Settings
Both scripts are configured for China region by default:
```python
DEMO_REGION = 'cn-northwest-1'
# DEMO_REGION = 'us-east-1'  # Alternative region
```

### Voice Settings (polly-play.py)
```python
VoiceId='Zhiyu'      # Chinese female voice
Engine='standard'    # or 'neural' for higher quality
```

### Language Settings (transcribe-mic.py)
```python
SOURCE_LANGCODE = 'zh-CN'  # Chinese Mandarin
# Other supported languages: en-US, en-GB, ja-JP, ko-KR, etc.
```

## China Region Support

For China region usage, Amazon Transcribe requires endpoint modification:

**File**: `amazon_transcribe/endpoints.py`
```python
class _TranscribeRegionEndpointResolver(BaseEndpointResolver):
    async def resolve(self, region: str) -> str:
        """Apply region to transcribe uri template."""
        if region not in ['cn-northwest-1', 'cn-north-1']:
            return f"https://transcribestreaming.{region}.amazonaws.com"
        else:
            return f"https://transcribestreaming.{region}.amazonaws.com.cn"
```

## Troubleshooting

### Common Issues
- **Microphone not detected**: Check system audio permissions
- **Audio playback fails**: Ensure ffmpeg is properly installed
- **Transcription not working**: Verify AWS credentials and region settings
- **China region issues**: Apply the endpoint modification above

## License

This project is licensed under the Apache-2.0 License.
