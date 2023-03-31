#coding:utf8

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

class PromptManager(object):
    def __init__(self):
        pass
    
    def get_qa_prompt(self, context_text, query_text, reply_language='Chinese'):
        return DEFAULT_PROMPT_TEMPLATE.format(context_str="我叫东莞晨", query_str="我叫什么", reply_language=reply_language)
    

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