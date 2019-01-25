from django.shortcuts import render
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search,Document
from django.views.generic.base import View
from django.http.response import HttpResponse
from datetime import datetime
import json
# Create your views here.

client = Elasticsearch(hosts=['10.1.62.240:9200'])
class SearchView(View):

    def get(self,request):
        # 从请求获取查询关键词
        key_words = request.GET.get("q","")

        #从请求获取请求的页数
        page = request.GET.get("p","")

        try:
            page = int(page)
        except BaseException:
            page = 1
        start_time = datetime.now()
        response = client.search(
            index='policydoc',
            request_timeout=60,
            body={
                "query": {
                    "multi_match": {
                        "query": key_words,
                        "fields": ["title", "content"]
                    }
                },
                "from": (page - 1) * 10,
                "size": 1,
                "highlight": {
                    "pre_tags": ['<span class="keyWord">'],
                    "post_tags": ['</span>'],
                    "fields": {
                        "title": {},
                        "content": {},
                    }
                }
            }

        )
        # print(json.dumps(response,ensure_ascii=False))
        end_time = datetime.now()
        last_seconds = (end_time - start_time).total_seconds()
        hit_list = []
        error_nums = 0
        for hit in response["hits"]["hits"]:
            hit_dict = {}
            try:
                if "title" in hit["highlight"]:
                    hit_dict["title"] = "".join(hit["highlight"]["title"])
                else:
                    hit_dict["title"] = hit["_source"]["title"]
                if "content" in hit["highlight"]:
                    hit_dict["content"] = "".join(
                        hit["highlight"]["content"])
                else:
                    hit_dict["content"] = hit["_source"]["content"][:200]
                hit_dict["create_date"] = hit["_source"]["create_date"]
                hit_dict["link"] = hit["_source"]["link"]
                hit_dict["score"] = hit["_score"]
                hit_dict['source_site'] = hit["_source"]['organization']
                hit_dict['id'] = hit['_id']
                hit_list.append(hit_dict)
            except:
                error_nums = error_nums + 1
        total_nums = int(response["hits"]["total"])
        if (page % 10) > 0:
            page_nums = int(total_nums / 10) + 1
        else:
            page_nums = int(total_nums / 10)
        return render(request, "result.html", {"page": page,
                                               "all_hits": hit_list,
                                               "key_words": key_words,
                                               "total_nums": total_nums,
                                               "page_nums": page_nums,
                                               "last_seconds": last_seconds
                                               })

def index(request):
    return render(request,'index.html')

class DetailView(View):
    def get(self,request):
        id = int(request.GET.get("id",""))
        doc = Document.get(id=id,index='policydoc',using=client).to_dict()
        link = doc['link']
        return render(request,'detail.html',{'link':link})




