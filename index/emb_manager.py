import openai

class EmbManager(object):
    def __init__(self):
        openai.api_key = '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'
        pass
    
    def single_text_to_emb(self, text):
        datas = openai.Embedding.create(input=[text], model="text-embedding-ada-002").data
        # datas = sorted(datas, key=lambda x: x["index"])
        # print(datas)
        return datas[0]['embedding']

if __name__ == "__main__":
    test = EmbManager()
    emb = test.single_text_to_emb('325346')
    print(emb)