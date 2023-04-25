from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from chat.chat_manager import chat_instance
from chat.prompt_manager import PromptManager
from index.file_db_manager import FileDbManager
from django.core.cache import cache
from numpy.core.numeric import promote_types
import time
import json

def chat(request):
    # 获取请求参数
    # channel_id = request.GET.get('channel_id')
    # user_name = request.GET.get('user_name')
    index = request.GET.get('index')
    query = request.GET.get('query')

    t = time.time()
    prompt_manager = PromptManager(index)
    print("------- init prompt manager: " + str(time.time()-t))
    t = time.time()
    prompt = prompt_manager.construct_qa_prompt(query, token_limit = 1000, top_k = 40)
    print("------- get prompt: " + str(time.time()-t))
    # print (prompt)
    t = time.time()
    gpt_res = chat_instance.predict(prompt)
    print("------- predict: " + str(time.time()-t))
    response_data = {
        'gpt_res': gpt_res
    }
    

    return JsonResponse(response_data)

def index(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        print ('------------data', data)
        
        docs = data.get('docs', [])
        index_name = data.get('index')
        db_manager = FileDbManager(index_name)
        for doc in docs:
            db_manager.build_single_doc(doc.get('text'), doc.get('origin_info_id'))
        
        db_manager.save_to_disk()
        response_data = {
            'response': 'success'
        }
        return JsonResponse(response_data)
    else:
        response_data = {
            'response': 'error, should request using Post'
        }
        return JsonResponse(response_data)
