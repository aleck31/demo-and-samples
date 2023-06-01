#!/usr/bin/env python3
import boto3





def translate_txt(region_name, first_lang_text, sourch_langcode, target_langcode):
    client = boto3.client(service_name='translate', region_name=region_name, use_ssl=True)

    result = client.translate_text(
        Text=first_lang_text, 
        SourceLanguageCode=sourch_langcode, 
        TargetLanguageCode=target_langcode)
    # print('SourceLanguageCode: ' + result.get('SourceLanguageCode'))
    # print('TargetLanguageCode: ' + result.get('TargetLanguageCode'))

    return result.get('TranslatedText')
