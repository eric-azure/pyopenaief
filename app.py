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
    import argparse
    from pywebio.platform.tornado_http import start_server as start_http_server
    from pywebio import start_server as start_ws_server

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    parser.add_argument("--http", action="store_true", default=False, help='Whether to enable http protocol for communicates')
    args = parser.parse_args()

    if args.http:
        start_http_server(main, port=args.port)
    else:
        # Since some cloud server may close idle connections (such as heroku),
        # use `websocket_ping_interval` to  keep the connection alive
        start_ws_server(main, port=args.port, websocket_ping_interval=30)