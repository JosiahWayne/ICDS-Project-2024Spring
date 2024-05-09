import requests
import json

url = "https://openai.api2d.net/v1/chat/completions"

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer fk226555-DCh9BjnQ8juitfMYRT0Ypw12cknERR0f' # <-- 把 fkxxxxx 替换成你自己的 Forward Key，注意前面的 Bearer 要保留，并且和 Key 中间有一个空格。
}
context = ''
data = {
  "model": "gpt-3.5-turbo-0125",
  "messages": [{"role": "user", "content": "你好！给我讲个笑话。"}],
  "stream": False,
}


while True:
    pm = input("YOU:")
    prompt = pm + "\nAI:"
    data["messages"][0]["content"] = prompt
    response = requests.post(url, headers=headers, json=data)
    ans = response.json()
    print(ans)
    print(ans["choices"][0]["message"]['content'])




# def chat_with_gpt(input_message, conversation):
#     print('GPT-4: ', end='')
#     messages = conversation + [
#         {"role": "user", "content": input_message}
#     ]
#     completion = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo-16k",
#         # model = "gpt-4-1106-preview", #太贵，用不起了
#         messages=messages,
#         temperature = 0,
#         stream=True
#     )
#     response = []
#     for chunk in completion:
#         if 'content' in chunk['choices'][0]['delta']:
#             chunk_content = chunk['choices'][0]['delta']["content"]
#             print(chunk_content, end='')
#             response.append(chunk_content)
#     response = ''.join(response)