
This a simultaneous interpretation demo app, which monitor the voice of the client's microphone, use Amazon Transcribe convert the speech into text, then use Amazon Translate service translate it to a second language, finally call the Amazon Polly to read the translated text.



### Prerequisites
- AWS Account with sufficient [(IAM)](https://aws.amazon.com/iam/) permissions.
- [Python 3.10](https://www.python.org/downloads/) or later and
  [pip package installer](https://pip.pypa.io/en/stable/)

- Install python dependencies
    - `pip install -r ./requirements.txt`


### How to use


```shell
# run it
$ python ./app.py

# stop it
Ctrl + C
```

### Sample output
```shell
🔛 Say something 
🎙 Listening ...

今天星期五 🔚
translate from zh-CN to en-US
📢 

#Ctrl+C
🛑 Stop listening.
```


### About China Region support

> Due to the lack of Amazon translate services this demo cannot run in China Region.
> If you're trying to use transcribe function in China Region, please refer to  
> following instructions to add support for China region endpoint.

> file path: amazon_transcribe/endpoints.py

```python
# class _TranscribeRegionEndpointResolver(BaseEndpointResolver):
#     async def resolve(self, region: str) -> str:
#         """Apply region to transcribe uri template."""
#         return f"https://transcribestreaming.{region}.amazonaws.com"

# add China region endpoint support
class _TranscribeRegionEndpointResolver(BaseEndpointResolver):
    async def resolve(self, region: str) -> str:
        """Apply region to transcribe uri template."""
        if region.startswith('cn'):
            return f"https://transcribestreaming.{region}.amazonaws.com.cn"
        else:
            return f"https://transcribestreaming.{region}.amazonaws.com"
```
