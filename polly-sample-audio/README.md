
The script helps to generate Amazon Polly small sample audio files (total size < 3MB)
for all by Amazon Polly supported all languages, and all voices for each language for all engines (`neural` and `standard`),
or an individual engine.



### Prerequisites
- AWS Account with sufficient [(IAM)](https://aws.amazon.com/iam/) permissions.
- [Python 3.8](https://www.python.org/downloads/) or later and
  [pip package installer](https://pip.pypa.io/en/stable/)

- Install python dependencies
    - `pip install -r ./requirements.txt`


### How to use


```shell
$ python ./get-audio.py
```

### Sample output
```shell
synthesizing: ./audio/neural/German-de-DE-Vicki.mp3
synthesizing: ./audio/neural/German-de-AT-Hannah.mp3
synthesizing: ./audio/neural/German-de-DE-Daniel.mp3
...

synthesized 32 audio files for engine: neural


synthesizing: ./audio/standard/German-de-DE-Vicki.mp3
synthesizing: ./audio/standard/German-de-DE-Marlene.mp3
synthesizing: ./audio/standard/German-de-DE-Hans.mp3
...

synthesized 60 audio files for engine: standard
```
