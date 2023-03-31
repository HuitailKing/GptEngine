import pinecone
from emb_manager import EmbManager
from utils import get_md5

# initialize connection to pinecone (get API key at app.pinecone.io)

class DbManager(object):
    def __init__(self):
        self.type = 'pinecone'
        pinecone.init(
            api_key="eecd9ae4-2392-4643-8499-1d7baf5dd4d8",
            environment="eu-west1-gcp"
        )
        # check if 'openai' index already exists (only create index if not)
        if 'gpt-index-0331' not in pinecone.list_indexes():
            pinecone.create_index('gpt-index-0331', dimension=1536)
        # connect to index
        self.index = pinecone.Index('gpt-index-0331')
        self.emb_manager = EmbManager()


    def upsert_single_doc_to_vector_db(self, id, emb, meta):
        ids_batch = [id]
        embeds = [emb]
        metas = [meta]
        self.index.upsert(zip(ids_batch, embeds, metas))


    def build_single_doc(self, json_doc, tag=None):
        text = json_doc['text']
        docid = get_md5(text)
        emb = self.emb_manager.single_text_to_emb(text)

        meta = {}
        meta['docid'] = docid
        meta['tag'] = tag
        meta['text'] = text
        return self.upsert_single_doc_to_vector_db(docid, emb, meta)


    def query(self, query_text):
        query_emb = self.emb_manager.single_text_to_emb(query_text)
        filters = self.construct_filters('2')
        rsp = self.index.query(top_k=1, vector=query_emb, include_metadata=True, filter=filters)
        print(rsp)


    # filter: https://docs.pinecone.io/docs/metadata-filtering
    def construct_filters(self, tag_list):
        if not isinstance(tag_list, list):
            tag_list = [tag_list]

        return {
            'tag': {'$in': tag_list}
        }

if __name__ == "__main__":
    db_manager = DbManager()
    
    doc = {}
    doc['text'] = '我是测试text1'
    db_manager.build_single_doc(doc, tag='1')

    doc = {}
    doc['text'] = '我是测试text2'
    db_manager.build_single_doc(doc, tag='2')

    doc = {}
    doc['text'] = '我是测试text22'
    db_manager.build_single_doc(doc, tag='2')

    db_manager.query('测试')
