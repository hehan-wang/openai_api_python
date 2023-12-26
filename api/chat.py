from openai import OpenAI

from openai.types.chat import completion_create_params

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    response_format=completion_create_params.ResponseFormat(type="json_object")
)

print(completion.choices[0].message)
