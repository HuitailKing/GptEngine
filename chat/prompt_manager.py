#coding:utf8
from index.db_manager import DbManager
import tiktoken

DEFAULT_PROMPT_TEMPLATE = """\
This is a telegram channel of Jack, text is below.
---------------------
{context_str}
---------------------
Using the provided context information, write a comprehensive reply to the given query.
Use prior knowledge only if the given context didn't provide enough information.
Answer the question: {query_str}
Reply in {reply_language}
reply as much as possible.
"""

DEFAULT_PROMPT = DEFAULT_PROMPT_TEMPLATE.format(context_str="我叫董冠辰", query_str="我叫什么", reply_language="Chinese")

class PromptManager(object):
    def __init__(self, index_name='gpt-index-cut-v1'):
        self.db_manager = DbManager(index_name)
        self.encoding = tiktoken.get_encoding('cl100k_base')
        self.clean_prompt_token = len(self.encoding.encode(DEFAULT_PROMPT_TEMPLATE))

    
    def get_qa_prompt(self, query_str, context_str, reply_language='Chinese'):
        return DEFAULT_PROMPT_TEMPLATE.format(query_str=query_str, context_str=context_str,reply_language=reply_language)


    def construct_context(self, query_str, token_limit = 3600, top_k = 10):
        total_token_cnt = 0

        matches = self.db_manager.query(query_str, top_k)['matches']
        context = ""
        for match in matches:
            
            meta_data = match['metadata']
            cur_token_cnt = len(self.encoding.encode(meta_data['text']))
            print('--------> cur_token_cnt:%s, total_token_cnt:%s, clean_prompt_token:%s, token_limit:%s '%(cur_token_cnt, total_token_cnt, self.clean_prompt_token, token_limit))
            # 当前块太大，直接超过prompt，先跳过 TODO:太大块的切分
            if cur_token_cnt > token_limit:
                continue
            # 不大的块就多攒几个，攒够或者遍历完为止
            if (total_token_cnt + cur_token_cnt + self.clean_prompt_token < token_limit):
                total_token_cnt += cur_token_cnt
                context += meta_data['text']
        return context


    def construct_qa_prompt(self, query_str, top_k = 10, reply_language='Chinese'):
        context_str = self.construct_context(query_str, top_k=top_k)
        return self.get_qa_prompt(query_str, context_str, reply_language=reply_language)   


if __name__ == "__main__":
    prompt_manager = PromptManager()
    prompt = prompt_manager.construct_qa_prompt('PKM是什么')
    print (prompt)