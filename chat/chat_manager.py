#coding:utf8

import openai
from index.db_manager import DbManager
from 

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

DEFAULT_PROMPT = DEFAULT_PROMPT_TEMPLATE.format(context_str="我叫东莞晨", query_str="我叫什么", reply_language="Chinese")

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
        print(rsp['choices'][0]['message']['content'])

if __name__ == "__main__":
    chat_manager = ChatManager()
    
    chat_manager.predict()