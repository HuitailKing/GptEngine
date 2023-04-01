import pinecone
from index.emb_manager import EmbManager
from utils.util import get_md5
import time

# initialize connection to pinecone (get API key at app.pinecone.io)
# https://app.pinecone.io/organizations/-NRsC0fpT-k_CZv3LEVl/projects/eu-west1-gcp:8d8adfd/indexes/gpt-index-0331
class DbManager(object):
    def __init__(self, index_name='gpt-index-cut-v1'):
        self.type = 'pinecone'
        pinecone.init(
            api_key="eecd9ae4-2392-4643-8499-1d7baf5dd4d8",
            environment="eu-west1-gcp"
        )
        # check if 'openai' index already exists (only create index if not)
        if index_name not in pinecone.list_indexes():
            pinecone.create_index(index_name, dimension=1536)
        # connect to index
        # gpt-index-0331, gpt-index-cut-v1
        self.index = pinecone.Index(index_name)
        self.emb_manager = EmbManager()


    def upsert_single_doc_to_vector_db(self, id, emb, meta):
        ids_batch = [id]
        embeds = [emb]
        metas = [meta]
        self.index.upsert(zip(ids_batch, embeds, metas))


    def build_single_doc(self, text, tag_list=None, origin_info_id=None):
        # for tag in tag_list:
        #     text += "#" + tag
        docid = get_md5(text)
        print('[%s]--------- build doc : [%s]-------\n'%(time.time(), docid) + text)
        emb = self.emb_manager.single_text_to_emb(text)
        if not emb:
            return None

        meta = {}
        meta['docid'] = docid
        # meta['tag'] = tag_list
        meta['text'] = text
        if origin_info_id:
            meta['origin_info_id'] = origin_info_id
        return self.upsert_single_doc_to_vector_db(docid, emb, meta)

    def build_batch_docs(self, text_list):
        ids_batch = [get_md5(text) for text in text_list]
        
        print("-------> embedding caculating...")
        s_time = time.time()
        embs_batch = self.emb_manager.batch_texts_to_embs(text_list)
        r_time = time.time()
        print("-------> time cost:" + str(r_time - s_time))

        metas_batch = [{'text': text, 'docid':get_md5(text)} for text in text_list]
        to_upsert = zip(ids_batch, embs_batch, metas_batch)
        return self.index.upsert(vectors=list(to_upsert))

    def query(self, query_text, top_k=10):
        query_emb = self.emb_manager.single_text_to_emb(query_text)
        # filters = self.construct_filters('2')
        return self.index.query(top_k=top_k, vector=query_emb, include_metadata=True, filter=None)


    # filter: https://docs.pinecone.io/docs/metadata-filtering
    def construct_filters(self, tag_list):
        if not isinstance(tag_list, list):
            tag_list = [tag_list]

        return {
            'tag': {'$in': tag_list}
        }

if __name__ == "__main__":
    db_manager = DbManager()
    rsp = db_manager.query(' this was part of the original inspiration for me. A ')
    print (rsp)
