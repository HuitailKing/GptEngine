#coding:utf8

import openai
from index.telegram_manager import TelegramManager
from chat.prompt_manager import PromptManager

# Make sure to cite results using [number] notation after the reference.
# If the provided context information refer to multiple subjects with the same name, write separate answers for each subject.

# DEFAULT_PROMPT_TEMPLATE = """\
# Context information is below.
# ---------------------
# {context_str}
# ---------------------
# Using the provided context information, write a comprehensive reply to the given query.
# Use prior knowledge only if the given context didn't provide enough information.
# Answer the question: {query_str}
# Reply in {reply_language}
# reply as much as possible.
# """

# DEFAULT_PROMPT = DEFAULT_PROMPT_TEMPLATE.format(context_str="我叫董冠辰", query_str="我叫什么", reply_language="Chinese")

class ChatManager(object):
    def __init__(self):
        openai.api_key = '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'


    def predict(self, prompt=''):
        rsp = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'user', 'content': prompt}
            ],
            temperature=0,
        )
        print('================ GPT Response ================')
        print(rsp['choices'][0]['finish_reason'])
        print(rsp['choices'][0]['message']['content'])

# info粒度建库
def ai_func_v0():
    tg_manager = TelegramManager()
    chat_manager = ChatManager()
    # 建库
    prompt_manager_v0 = PromptManager('gpt-index-0331')
    # tg_manager.single_mode_process_v0()
    while True:
        query_str = input("================ 请输入query: ===============\n")
        # 构造prompt
        prompt = prompt_manager_v0.construct_qa_prompt(query_str, top_k=200)
        print("=================== GPT Prompt ==================")
        print(prompt)
        # 交互
        chat_manager.predict(prompt)

# 句子粒度建库
def compare():
    tg_manager = TelegramManager()
    chat_manager = ChatManager()
    # 建库
    prompt_manager_v0 = PromptManager('gpt-index-0331')
    prompt_manager_v1 = PromptManager('gpt-index-cut-v1')
    # tg_manager.single_mode_process_v1()
    while True:
        query_str = input("================ 请输入query: ===============\n")
        # 构造prompt
        prompt0 = prompt_manager_v0.construct_qa_prompt(query_str, top_k=200)
        prompt1 = prompt_manager_v1.construct_qa_prompt(query_str, top_k=200)
        
        print("=================== GPT V0 ==================")
        print (prompt0)
        chat_manager.predict(prompt0)
        print("=================== GPT V1 ==================")
        print (prompt1)
        chat_manager.predict(prompt1)

if __name__ == "__main__":
    
    compare()