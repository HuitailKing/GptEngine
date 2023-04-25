import openai
import time

class EmbManager(object):
    def __init__(self):
        openai.api_key = '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'
        pass
    

    def single_text_to_emb(self, text):
        for i in range(5):
            try:
                datas = openai.Embedding.create(input=[text], model="text-embedding-ada-002").data
                return datas[0]['embedding']
            except Exception as e:
                print(e)
                time.sleep(5)
                return None
        # datas = sorted(datas, key=lambda x: x["index"])
        # print(datas)
        
    

    def batch_texts_to_embs(self, texts):
        return openai.Embedding.create(input=texts, model="text-embedding-ada-002").data

if __name__ == "__main__":
    test = EmbManager()
    emb = test.single_text_to_emb('325346')
    print(emb)