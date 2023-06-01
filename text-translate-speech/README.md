
This demo app monitor the voice of the microphone, use Amazon Transcribe convert the speech into text, then use Amazon Translate service translate it to a second language, finally call the Amazon Polly to read the translated text.



### Prerequisites
- AWS Account with sufficient [(IAM)](https://aws.amazon.com/iam/) permissions.
- [Python 3.10](https://www.python.org/downloads/) or later and
  [pip package installer](https://pip.pypa.io/en/stable/)

- Install python dependencies
    - `pip install -r ./requirements.txt`


### How to use


```shell
$ python ./app.py
```

### Sample output
```shell
今天星期五
🔚
```
