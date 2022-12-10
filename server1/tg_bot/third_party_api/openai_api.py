import openai

from server1.tg_bot._secret import openai_key

openai.api_key = openai_key


def generate_response(message):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=message,
        temperature=0.5,
        max_tokens=180,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response["choices"][0]["text"]
