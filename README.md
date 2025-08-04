# AWS AI Services Demo Collection

A comprehensive collection of demos showcasing AWS AI services including Amazon Polly (Text-to-Speech), Amazon Transcribe (Speech-to-Text), and Amazon Translate.

## 📁 Projects Overview

### 🎙️ [polly-sample-audio](./polly-sample-audio/)
**Batch Audio Generation Tool**
- Generates sample audio files for **all 4 Polly engines**: Standard, Neural, Generative, Long-form
- Supports 40+ languages with 147 total voice samples
- Perfect for comparing voice quality across different engines
- **Output**: 4.4MB of organized audio samples by engine type

```bash
cd polly-sample-audio
python generate_samples.py
```

### 🎛️ [polly-interactive-demo](./polly-interactive-demo/)
**Interactive Voice Testing Tool**
- Real-time voice synthesis with customizable text input
- Interactive selection of engines, languages, and voices
- Instant audio playback for testing
- Supports custom text or predefined language samples

```bash
cd polly-interactive-demo
python polly_demo.py
```

### 🎤 [text-speech-conversion](./text-speech-conversion/)
**Bidirectional Text-Speech Conversion Tools**
- **transcribe-mic.py**: Real-time microphone transcription using Amazon Transcribe
- **polly-play.py**: Text-to-speech synthesis using Amazon Polly
- Supports multiple languages and voice options
- Includes China region endpoint support for Transcribe

```bash
cd text-speech-conversion
python transcribe-mic.py  # Speech-to-text
python polly-play.py      # Text-to-speech
```

### 🌐 [text-translate-speech](./text-translate-speech/)
**Simultaneous Interpretation Demo**
- Real-time speech translation pipeline: Speech → Text → Translate → Speech
- Monitors microphone input continuously
- Combines Transcribe + Translate + Polly services
- **Note**: Requires regions with Amazon Translate support (not available in China regions)

```bash
cd text-translate-speech
python app.py
```

## 🚀 Quick Start

### Prerequisites
- AWS Account with sufficient [IAM permissions](https://aws.amazon.com/iam/)
- [Python 3.10+](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/)
- AWS credentials configured (via AWS CLI, environment variables, or IAM roles)

### Setup
```bash
# Clone and navigate to the project
git clone <repository-url>
cd demo-and-samples

# Create and activate virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Choose Your Demo
```bash
# For batch audio generation
cd polly-sample-audio && python generate_samples.py

# For interactive voice testing  
cd polly-interactive-demo && python polly_demo.py

# For speech recognition
cd text-speech-conversion && python transcribe-mic.py

# For real-time translation
cd text-translate-speech && python app.py
```

## 🌍 Regional Considerations

### Engine Availability by Region
| Region | Standard | Neural | Generative | Long-form |
|--------|----------|--------|------------|-----------|
| **us-east-1** | ✅ | ✅ | ✅ | ✅ |
| **eu-central-1, us-west-2** | ✅ | ✅ | ✅ | ❌ |
| **Most regions** | ✅ | ✅ | ❌ | ❌ |
| **cn-northwest-1** | ✅ | ❌ | ❌ | ❌ |

### Service Availability
- **Amazon Polly**: Available in most AWS regions
- **Amazon Transcribe**: Available in most regions (China regions require endpoint modification)
- **Amazon Translate**: **Not available in China regions**

## 💰 Cost Considerations

**Approximate costs per 1M characters:**
- Standard: ~$4
- Neural: ~$16  
- Generative: ~$30
- Long-form: ~$100

*Check [AWS Polly Pricing](https://aws.amazon.com/polly/pricing/) for current rates.*

## 📋 Project Structure
```
demo-and-samples/
├── polly-sample-audio/          # Batch audio generation
├── polly-interactive-demo/      # Interactive voice testing
├── text-speech-conversion/      # Bidirectional text-speech tools
├── text-translate-speech/       # Real-time translation
├── requirements.txt             # Shared dependencies
└── README.md                    # This file
```

## 🔧 Troubleshooting

### Common Issues
- **Region not supported**: Switch to `us-east-1` for full engine support
- **High costs**: Avoid Generative/Long-form engines for large-scale testing
- **China region**: Only Standard engine supported for Polly; Translate not available

### Getting Help
Each sub-project contains detailed README files with specific setup instructions and troubleshooting guides.

## 📄 License

This project is licensed under the Apache-2.0 License.
