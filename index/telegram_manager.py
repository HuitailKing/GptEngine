import os
import logging
import re
import openai
import json
import tiktoken
import hashlib
from utils.util import get_md5
# from index.db_manager import DbManager
from index.file_db_manager import FileDbManager
import logging
import time

class TelegramManager(object):
    def __init__(self):
        self.tokenizer = tiktoken.get_encoding('cl100k_base')

    def get_documents(self, index_name="jackzone_sample"):
        file = "/Users/bytedance/Documents/repo/gpt/GptEngine/index/data/" + index_name + ".json"
        documents = []
        index_name = ""
        logging.debug("Loading documents...")
        if os.path.splitext(file)[1] == ".pdf":
            logging.debug("Loading PDF...")
            CJKPDFReader = download_lo
            ader("CJKPDFReader")
            loader = CJKPDFReader()
            documents = loader.load_data(file=file)
        if os.path.splitext(file)[1] == ".json":
            import json
            with open(file, 'r') as f:
                # 加载JSON数据
                data = json.load(f)['info']
            return data
        return []


    def single_mode_process_v1(self, start_idx=0):
        db_manager = FileDbManager('jacksample')
        start_time = time.time()
        origin_doc_list = self.get_documents()
        try:
            for idx, doc in enumerate(origin_doc_list):
                if idx < start_idx:
                    continue
                if doc['type'] != 'Text':
                    continue
                print('---------------------------> doc cnt:' + str(idx)) 
                text = doc['content']['body']
                text = text.strip()
                text = text.replace(' ', '')
                if not text:
                    continue
                text_splits = text.split('\n')
                for split in text_splits:
                    if not split:
                        continue
                    db_manager.build_single_doc(split, doc['tags'], origin_info_id=doc['id'])
        except Exception as e:
            # openai可能限速 maybe需要充钱
            print(e)
            time.sleep(2)
        end_time = time.time()
        print("========== process time:" + str(end_time - start_time))
        db_manager.save_to_disk()

    # info粒度建库
    def single_mode_process_v0(self, index_name="jackzone_sample"):
        start_time = time.time()
        origin_doc_list = self.get_documents(index_name)
        db_manager = FileDbManager(index_name)
        not_text_cnt = 0
        succ_cnt = 0
        fail_cnt = 0
        try:
            for idx, doc in enumerate(origin_doc_list):
                if doc['type'] != 'Text':
                    not_text_cnt += 1
                    continue
                print('---------------------------> doc cnt:' + str(idx)) 
                text = doc['content']['body']
                
                ret = db_manager.build_single_doc(text, doc['tags'], origin_info_id=doc['id'])
                if ret:
                    succ_cnt += 1
                else:
                    fail_cnt += 1
                # time.sleep(0.9)
        except Exception as e:
            # openai可能限速 maybe需要充钱
            print(e)
            time.sleep(2)
        end_time = time.time()
        print("========== process time:" + str(end_time - start_time) + " total:" + str(len(origin_doc_list)) + " success:" + str(succ_cnt) + " failed:" + str(fail_cnt) + " not_text:" + str(not_text_cnt))
        db_manager.save_to_disk()

    def batch_mode_process(self, batch_size=2):
        
        origin_doc_list = self.get_documents()
        text_list = []
        batch_cnt = 1
        for doc in origin_doc_list:
            if doc['type'] != 'Text':
                continue
            text_list.append(doc['content']['body'])
            if len(text_list) >= batch_size:
                print("batch[%s]========== processing..."%batch_cnt)
                start_time = time.time()
                self.db_manager.build_batch_docs(text_list)
                end_time = time.time()
                print("batch[%s]========== process time:"%batch_cnt + str(end_time - start_time))
                text_list = []
                batch_cnt += 1
        self.db_manager.build_batch_docs(text_list)


if __name__ == "__main__":
    # 测试tg格式数据建库
    tg_manager = TelegramManager()
    tg_manager.single_mode_process_v0("jackzone_full")