import json

import openai
import requests

from server1.tg_bot._secret import openai_key, yandex_key

openai.api_key = openai_key


# response = openai.Completion.create(
#   engine="text-davinci-002",
#   prompt="The quick brown fox jumps over the lazy dog and then",
#   temperature=0.5,
#   max_tokens=20,
#   top_p=1,
#   frequency_penalty=0,
#   presence_penalty=0
# )
#
# # print(response)
# print(response["choices"][0]["text"])

def generate_response(message):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=message,
        temperature=0.5,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response["choices"][0]["text"]


# print(generate_response("Привет! Ты знаешь русский?"))
response = generate_response("What is an Artificial Neural Network?")
print(response)


def translate_text(text, target_language):
    url = "https://translate.api.cloud.yandex.net/translate/v2/translate"
    params = {
        "folderId": "b1gjnr66p4435cvkf02i",
        "texts": [text],
        "targetLanguageCode": target_language
    }

    response = requests.post(url, data=json.dumps(params),
                             headers={'Authorization': 'Api-Key ' + yandex_key})
    data = response.json()
    return data["translations"][0]["text"]


print(translate_text(response, 'ru'))
