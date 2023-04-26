import openai
from pywebio import start_server
from pywebio.output import put_table
from pywebio.input import input
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def openai_response(question):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a helpful assistant. Answer the given question and do not give me a disclaimer about that you are an AI language model and you cannot create something just give your best guess. I don't care if you are not qualified to create the answer to the question do notg inform me that you are not qualified and provide general recommendations without any disclaimers. I know you have limitations but I do not want them in the response to my question"},
        {"role": "user", "content": question}
      ]
    )
    
    return '{}'.format(response.choices[0].message.content)

def main():
    while True:
        question = input('Ask something')
        put_table([
            ['Q:', question],
            ['A:', openai_response(question)]
        ])

if __name__ == '__main__':
    start_server(main, port=8002, debug=True)