## Readme for transcribe-mic script

> If you use the transcribe service in China Region, please refer to following 
> instructions to add support for the endpoint in China.

> file path: amazon_transcribe/endpoints.py

```
# class _TranscribeRegionEndpointResolver(BaseEndpointResolver):
#     async def resolve(self, region: str) -> str:
#         """Apply region to transcribe uri template."""
#         return f"https://transcribestreaming.{region}.amazonaws.com"

# add China region endpoint support
class _TranscribeRegionEndpointResolver(BaseEndpointResolver):
    async def resolve(self, region: str) -> str:
        """Apply region to transcribe uri template."""
        if region not in ['cn-northwest-1', 'cn-north-1']:
            return f"https://transcribestreaming.{region}.amazonaws.com"
        else:
            return f"https://transcribestreaming.{region}.amazonaws.com.cn"
```
