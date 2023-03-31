from llama_index import download_loader
from llama_index import (
    Document,
    LLMPredictor,
    PromptHelper,
    QuestionAnswerPrompt,
    RefinePrompt,
)
import os
import logging
import re
import openai
import json
import tiktoken
import hashlib
from utils import get_md5


class TelegramPreprocessor(object):

    def __init__(self):
        self.tokenizer = tiktoken.get_encoding('cl100k_base')

    def add_space(self, text):
        punctuations = {"，": "， ", "。": "。 ", "？": "？ ", "！": "！ ", "：": "： ", "；": "； "}
        for cn_punc, en_punc in punctuations.items():
            text = text.replace(cn_punc, en_punc)
        return text

    def get_documents(self, file="/Users/bytedance/Documents/repo/gpt/GptEngine/index/jackzone.json"):
        documents = []
        index_name = ""
        logging.debug("Loading documents...")
        if os.path.splitext(file)[1] == ".pdf":
            logging.debug("Loading PDF...")
            CJKPDFReader = download_loader("CJKPDFReader")
            loader = CJKPDFReader()
            documents = loader.load_data(file=file)
        if os.path.splitext(file)[1] == ".json":
            import json
            with open('/Users/bytedance/Documents/repo/gpt/GptEngine/index/jackzone.json', 'r') as f:
                # 加载JSON数据
                data = json.load(f)['info']
            return data 
        return []
        # else:
        #     logging.debug("Loading text file...")
        #     with open(file, "r", encoding="utf-8") as f:
        #         text = self.add_space(f.read())
        #         documents += [Document(text)]
        # return documents[0].get_text()

    # def split_documents(self, s):
    #     return s.split('.')

    # def splits_to_embedding(self, splits):
    #     openai.api_key = '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'
    #     datas = openai.Embedding.create(input=splits, model="text-embedding-ada-002").data
    #     datas = sorted(datas, key=lambda x: x["index"])
    #     # print(datas)
    #     return datas

    # def build(self, splits, datas):
    #     index = {}
        
    #     forward_index = {}
    #     inverted_index = {}
    #     for docid, text in enumerate(splits):
    #         forward_index[docid] = text
    #     for data in datas:
    #         print(data['index'])
    #         # print (data['embedding'])
    #         inverted_index[data['index']] = data['embedding']
    #     index['forward_index'] = forward_index
    #     index['inverted_index'] = inverted_index

    # def build_index(self):
    #     # 拿到所有文档
    #     docs = self.get_documents()
    #     for doc in docs:
    #         print(get_md5(doc['content']['body']))
    #     splits = self.split_documents(text)
    #     print(len(splits))
    #     datas = self.splits_to_embedding(splits)
    #     self.build(splits, datas)

# def get_topk_embeddings(data):
    
#     pass
    

# def similarity(
#     embedding1: List,
#     embedding2: List,
#     mode: 'cosine',
# ) -> float:
#     """Get embedding similarity."""
#     if model == 'cpsine':
#         product = np.dot(embedding1, embedding2)
#         norm = np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
#         return product / norm
#     return 0
#     # print(data)

    


if __name__ == "__main__":
    a = TelegramPreprocessor()
    # a.build_index()s
    # build_index()