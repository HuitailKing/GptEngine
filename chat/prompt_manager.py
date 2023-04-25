#coding:utf8
# from index.db_manager import DbManager
from index.file_db_manager import FileDbManager
import tiktoken
import time
import logging

DEFAULT_PROMPT_TEMPLATE = """\
This is a telegram channel of Jack, text is below.
---------------------
{context_str}
---------------------
Using the provided context information, write a comprehensive reply to the given query.
Use prior knowledge only if the given context didn't provide enough information.
Answer the question: {query_str}
Reply in {reply_language}
reply at least 500 tokens.
"""

DEFAULT_PROMPT = DEFAULT_PROMPT_TEMPLATE.format(context_str="我叫董冠辰", query_str="我叫什么", reply_language="Chinese")

class PromptManager(object):
    def __init__(self, index_name='jack_full'):
        t0 = time.time()
        self.db_manager = FileDbManager(index_name)
        logging.info("------------db:" +  str(time.time()-t0))
        t1 = time.time()
        self.encoding = tiktoken.get_encoding('cl100k_base')
        self.clean_prompt_token = len(self.encoding.encode(DEFAULT_PROMPT_TEMPLATE))
        logging.info("------------prom:" +  str(time.time()-t1))

    
    def get_qa_prompt(self, query_str, context_str, reply_language='Chinese'):
        return DEFAULT_PROMPT_TEMPLATE.format(query_str=query_str, context_str=context_str,reply_language=reply_language)


    def construct_context(self, query_str, token_limit = 2000, top_k = 10):
        total_token_cnt = 0

        matches = self.db_manager.query(query_str, top_k)
        context = ""
        for match in matches:
            text = match['text']
            # print ("------get text" + text)
            cur_token_cnt = len(self.encoding.encode(text))
            # print('--------> cur_token_cnt:%s, total_token_cnt:%s, clean_prompt_token:%s, token_limit:%s '%(cur_token_cnt, total_token_cnt, self.clean_prompt_token, token_limit))
            # 当前块太大，直接超过prompt，先跳过 TODO:太大块的切分
            if cur_token_cnt > token_limit:
                continue
            # 不大的块就多攒几个，攒够或者遍历完为止
            if (total_token_cnt + cur_token_cnt + self.clean_prompt_token < token_limit):
                total_token_cnt += cur_token_cnt
                context += text
        return context


    def construct_qa_prompt(self, query_str, token_limit = 2000, top_k = 10, reply_language='Chinese'):
        context_str = self.construct_context(query_str, token_limit=token_limit, top_k=top_k)
        return self.get_qa_prompt(query_str, context_str, reply_language=reply_language)   


if __name__ == "__main__":
    prompt_manager = PromptManager()
    prompt = prompt_manager.construct_qa_prompt('PKM是什么')
    print (prompt)