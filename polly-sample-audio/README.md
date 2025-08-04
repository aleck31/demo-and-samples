# Amazon Polly TTS (Text to Speech) Sample Audio Generator

This script generates Amazon Polly sample audio files for all supported languages and voices across **all four engines**: `standard`, `neural`, `generative`, and `long-form`.

It supports 40+ languages including Chinese (Mandarin and Cantonese), with over 100 different voices to choose from across different engines.

## 🎙️ Amazon Polly Engine Comparison

| Engine | Quality | Cost | Use Cases | Voices | Region Support |
|--------|---------|------|-----------|--------|----------------|
| **Standard** | Basic | Lowest | Basic TTS, cost-sensitive apps | 61 voices | Global |
| **Neural** | Natural | Moderate | Daily apps, customer service | 60 voices | Most regions |
| **Generative** | Most human-like | Higher | Conversational AI, marketing | 20 voices | 3 regions only |
| **Long-form** | Premium for long content | Highest | News, podcasts, audiobooks | 6 voices | us-east-1 only |

### 📢 **Standard Engine**
- **Technology**: Traditional concatenative TTS
- **Features**: Reliable, cost-effective, widely supported
- **Best for**: Basic announcements, cost-sensitive applications
- **Languages**: 40+ languages
- **Regions**: All AWS regions

### 🧠 **Neural Engine**
- **Technology**: Advanced neural networks for natural speech
- **Features**: More natural than standard, good balance of quality and cost
- **Best for**: General applications, mobile apps, IVR systems
- **Languages**: 40+ languages
- **Regions**: Most AWS regions

### 🤖 **Generative Engine**
- **Technology**: Billion-parameter transformer model with LLM capabilities
- **Features**: Most human-like, emotionally engaged, adaptive conversational voices
- **Best for**: Virtual assistants, customer support, marketing content
- **Languages**: English, Spanish, French, German, Italian
- **Regions**: `us-east-1`, `eu-central-1`, `us-west-2`

### 📚 **Long-form Engine**
- **Technology**: Deep learning TTS optimized for extended content
- **Features**: Highly expressive, emotionally adept, context-aware emphasis
- **Best for**: News articles, training materials, podcasts, audiobooks
- **Languages**: English US, Spanish Spain
- **Regions**: `us-east-1` only

## Prerequisites

- AWS Account with sufficient [IAM permissions](https://aws.amazon.com/iam/)
- [Python 3.10](https://www.python.org/downloads/) or later
- [pip package installer](https://pip.pypa.io/en/stable/)
- Install dependencies: `pip install -r ./requirements.txt`

## 🚀 Quick Start

```shell
$ python ./generate_samples.py
```

**Sample output:**
```shell
🎙️  Amazon Polly TTS Engine Information:
==================================================
  📢 Standard: Traditional TTS, lowest cost
  🧠 Neural: More natural voices, moderate cost
  🤖 Generative: Most human-like, conversational (Higher cost)
  📚 Long-form: Optimized for long content, premium quality (Highest cost)

⚠️  WARNING: Premium engines have significantly higher costs!
   Premium engines in use: generative, long-form
   Check AWS Polly pricing: https://aws.amazon.com/polly/pricing/

🌍 Region: us-east-1
📁 Output directory: ./audio_samples
==================================================

synthesizing: ./audio_samples/standard/Chinese Mandarin-cmn-CN-Zhiyu.mp3
synthesizing: ./audio_samples/neural/English-en-US-Joanna.mp3
synthesizing: ./audio_samples/generative/English-en-US-Danielle.mp3
synthesizing: ./audio_samples/long-form/English-en-US-Gregory.mp3
...

synthesized 61 audio files for engine: standard
synthesized 60 audio files for engine: neural
synthesized 20 audio files for engine: generative
synthesized 6 audio files for engine: long-form

Total: 147 audio files generated (4.4MB)
```

## ⚙️ Configuration

### Region Configuration

The script defaults to `us-east-1` to support all four engines. You can modify the region in `generate_samples.py`:

```python
# Default (supports all engines)
DEMO_REGION = 'us-east-1'

# Alternative configurations:
# DEMO_REGION = 'eu-central-1'     # Supports: standard, neural, generative
# DEMO_REGION = 'us-west-2'        # Supports: standard, neural, generative  
# DEMO_REGION = 'ap-southeast-1'   # Supports: standard, neural only
# DEMO_REGION = 'cn-northwest-1'   # Supports: standard only (China region)
```

**⚠️ Note**: Voice availability varies by region. The numbers shown above (61/60/20/6) are specific to `us-east-1`. Other regions may have different voice counts.

### Engine Selection

Modify the `ENGINES` list to select specific engines:

```python
# All engines (default)
ENGINES = ['standard', 'neural', 'generative', 'long-form']

# Cost-conscious setup
ENGINES = ['standard', 'neural']

# Premium quality only
ENGINES = ['generative', 'long-form']

# Single engine testing
ENGINES = ['neural']
```

## 💰 Cost Considerations

**⚠️ Important**: Generative and Long-form engines have significantly higher costs than Standard and Neural engines.

- **Standard**: ~$4 per 1M characters
- **Neural**: ~$16 per 1M characters  
- **Generative**: ~$30 per 1M characters
- **Long-form**: ~$100 per 1M characters

*Prices are approximate. Check [AWS Polly Pricing](https://aws.amazon.com/polly/pricing/) for current rates.*

## 📁 Output Structure

```
samples/
├── standard/
│   ├── English-en-US-Joanna.mp3
│   ├── Chinese Mandarin-cmn-CN-Zhiyu.mp3
│   └── ...
├── neural/
│   ├── English-en-US-Joanna.mp3
│   ├── Cantonese-yue-CN-Hiujin.mp3
│   └── ...
├── generative/
│   ├── English-en-US-Danielle.mp3
│   ├── French-fr-FR-Lea.mp3
│   └── ...
└── long-form/
    ├── English-en-US-Gregory.mp3
    ├── Spanish-es-ES-Alba.mp3
    └── ...
```

## 🌍 Supported Languages by Engine

### Standard & Neural Engines
- **European Languages**: English (multiple variants), Spanish, French, German, Italian, Portuguese, Dutch, Polish, Romanian
- **Asian Languages**: Chinese (Mandarin), Japanese, Korean  
- **Nordic Languages**: Swedish, Norwegian, Danish, Icelandic
- **Other Languages**: Arabic, Turkish, Russian, Welsh

### Neural Engine Additional
- **Chinese Variants**: Cantonese (yue-CN-Hiujin)
- **Regional Variants**: More English variants (Singapore, Ireland, South Africa, New Zealand)

### Generative Engine (Premium)
- **English**: 9 voices (US, UK, Australian, Indian, South African)
- **Spanish**: 6 voices (US, Mexico, Spain)  
- **French**: 2 voices (France)
- **German**: 2 voices (Germany)
- **Italian**: 1 voice (Italy)

### Long-form Engine (Ultra-Premium)
- **English (US)**: 4 specialized voices (Danielle, Gregory, Patrick, Ruth)
- **Spanish (Spain)**: 2 specialized voices (Alba, Raul)

## 🔧 Troubleshooting

### Region Not Supported Error
```
ClientError: The requested engine is not supported in this region
```
**Solution**: Change `DEMO_REGION` to a supported region or remove unsupported engines from `ENGINES` list.

### High Costs Warning
If you see unexpectedly high AWS bills, check if you're using `generative` or `long-form` engines for large-scale testing.

### Voice Not Available
Some voices are only available in specific engines. The script automatically filters voices based on engine support.

## 📊 Performance Comparison

Based on actual generation results with typical language samples:

| Engine | Voices Generated | Avg File Size | Storage Used | Quality Score |
|--------|------------------|---------------|--------------|---------------|
| Standard | 61 voices | ~28KB | 1.9MB | 3/5 |
| Neural | 60 voices | ~28KB | 1.8MB | 4/5 |
| Generative | 20 voices | ~27KB | 592KB | 5/5 |
| Long-form | 6 voices | ~30KB | 200KB | 5/5 |

**Total Generated**: 147 audio files (4.4MB total)

## License

This project is licensed under the Apache-2.0 License.
