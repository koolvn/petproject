import json
import requests

from .._secret import yandex_key


def translate_text(text, target_language):
    url = "https://translate.api.cloud.yandex.net/translate/v2/translate"
    params = {
        "folderId": "b1gjnr66p4435cvkf02i",
        "texts": [text],
        "targetLanguageCode": target_language
    }

    response = requests.post(url, data=json.dumps(params),
                             headers={'Authorization': f'Api-Key {yandex_key}'})
    data = response.json()
    return data["translations"][0]["text"]
