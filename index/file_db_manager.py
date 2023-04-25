import pinecone
from index.emb_manager import EmbManager
from utils.util import get_md5, get_top_k_embeddings
import time
import json
import os
from matplotlib import path


# initialize connection to pinecone (get API key at app.pinecone.io)
# https://app.pinecone.io/organizations/-NRsC0fpT-k_CZv3LEVl/projects/eu-west1-gcp:8d8adfd/indexes/gpt-index-0331
class FileDbManager(object):
    def __init__(self, index_name='jackzone_sample'):
        self.type = 'file'
        self.index = {"vector_index":{}, "meta_index": {}}
        self.emb_manager = EmbManager()
        self.index_name = index_name
        
        abs_path = os.path.abspath(__file__)
        dir_path = os.path.dirname(abs_path)
        self.path = dir_path + '/file_index_data/' + self.index_name + ".json"
        print(self.path)

        if os.path.exists(self.path):
            print ("exist file" + self.path)
            with open(self.path, 'r') as f:
                # 加载JSON数据
                self.index = json.load(f)
                # print(self.index)
            
            


    def build_single_doc(self, text, tag_list=None, origin_info_id=None):
        if not origin_info_id:
            docid = get_md5(text)
        else:
            docid = origin_info_id
        print('[%s]--------- build doc : [%s]-------\n'%(time.time(), docid) + text)
        emb = self.emb_manager.single_text_to_emb(text)
        if not emb:
            return False

        meta = {}
        meta['docid'] = docid
        meta['text'] = text
        if origin_info_id:
            meta['origin_info_id'] = origin_info_id
        self.index['meta_index'][docid] = meta
        self.index['vector_index'][docid] = emb
        return True


    def query(self, query_text, top_k=3):
        start_time = time.time()
        query_emb = self.emb_manager.single_text_to_emb(query_text)
        print( "==========query to emb time:" + str(time.time()- start_time))
        start_time = time.time()
        similarities, ids = get_top_k_embeddings(query_emb, self.index, similarity_top_k=top_k)
        match_list = []
        for i in range(len(ids)):
            id = ids[i]
            similarity = similarities[i]
            match_doc = self.index['meta_index'][id]
            match_doc['score'] = similarity
            match_list.append(match_doc)
            # print('----- get similarity')
            # print(match_doc)

        end_time = time.time()
        print( "==========query time:" + str(end_time- start_time))
        return  match_list


    def save_to_disk(self):
        if not os.path.exists(self.path):
            open(self.path, "w").close()   # 创建空文件
        with open(self.path, "w") as f:
            f.write(json.dumps(self.index))


if __name__ == "__main__":
    db_manager = FileDbManager("jacksample")
    # db_manager.build_single_doc("我是一个")
    rsp = db_manager.query(' this was part of the original inspiration for me. A ')
    db_manager.save_to_disk()
    print (rsp)
