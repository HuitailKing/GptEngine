#coding:utf8

import openai
from index.telegram_manager import TelegramManager
from chat.prompt_manager import PromptManager

DEFAULT_PROMPT_TEMPLATE = """\
Context information is below.
---------------------
{context_str}
---------------------
Using the provided context information, write a comprehensive reply to the given query.
Make sure to cite results using [number] notation after the reference.
If the provided context information refer to multiple subjects with the same name, write separate answers for each subject.
Use prior knowledge only if the given context didn't provide enough information.
Answer the question: {query_str}
Reply in {reply_language}
"""

DEFAULT_PROMPT = DEFAULT_PROMPT_TEMPLATE.format(context_str="我叫董冠辰", query_str="我叫什么", reply_language="Chinese")

class ChatManager(object):
    def __init__(self):
        openai.api_key = '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'
    

    def predict(self, prompt=DEFAULT_PROMPT):
        rsp = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'user', 'content': prompt}
            ],
            temperature=0,
        )
        print('================ GPT Response ================')
        print(rsp['choices'][0]['message']['content'])

if __name__ == "__main__":
    tg_manager = TelegramManager()
    prompt_manager = PromptManager()
    chat_manager = ChatManager()

    # 建库
    tg_manager.single_mode_process_v1()

    while True:
        query_str = input("================ 请输入query: ===============\n")
        # 构造prompt
        # query_str = '技爆发面前，追求效率已经成为了一种自发'
        prompt = prompt_manager.construct_qa_prompt(query_str, top_k=20)
        print("=================== GPT Prompt ==================")
        print(prompt)

        # 交互
        chat_manager.predict(prompt)