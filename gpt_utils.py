import requests
import json

import threading
import select
from chat_utils import *
import time

url = "https://openai.api2d.net/v1/chat/completions"
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer fk226555-DCh9BjnQ8juitfMYRT0Ypw12cknERR0f' # API Key
}
context = ''
data = {
  "model": "gpt-3.5-turbo-0125",
  "messages": [{"role": "user", "content": ""}],
  "stream": False,
}

def chattoGPT(context, msg=''):
    pm = context + msg
    prompt = pm + "\nAI:"
    data["messages"][0]["content"] = prompt
    response = requests.post(url, headers=headers, json=data)
    ans = response.json()
    return ans["choices"][0]["message"]['content']