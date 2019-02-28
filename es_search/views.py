import threading

from django.shortcuts import render
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Document
from django.views.generic.base import View
from django.http.response import HttpResponse
from django.forms.models import model_to_dict
from datetime import datetime
from .models import RelationPolicies, PolicyType, SearchDetailRecord, PolicyRecommend, Hotarticle
from django.db.models import Count

import json
import redis

# Create your views here.
redis_cli = redis.Redis(host='127.0.0.1', port=6379)
client = Elasticsearch(hosts=['10.1.62.240:9200'])


class SearchView(View):
    def get(self, request):
        # 从请求获取查询关键词
        key_words = request.GET.get("q", "")
        # 实现搜索关键词keyword加1操作
        redis_cli.zincrby("search_keywords_set", amount=1, value=key_words)
        # 获取topn关键词
        topn_search_clean = []
        topn_search = redis_cli.zrevrangebyscore(
            "search_keywords_set", "+inf", "-inf", start=0, num=5)
        for topn_key in topn_search:
            topn_key = str(topn_key, encoding="utf-8")
            topn_search_clean.append(topn_key)
        topn_search = topn_search_clean

        # 从请求获取请求的页数
        page = request.GET.get("p", "")
        try:
            page = int(page)
        except BaseException:
            page = 1
        start_time = datetime.now()
        response = client.search(
            index='policynew',
            request_timeout=60,
            body={
                "query": {
                    "multi_match": {
                        "query": key_words,
                        "fields": ["title", "content"],
                        "analyzer": "ik_smart"

                    }
                },
                "from": (page - 1) * 10,
                "size": 10,
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
        # print(len(response["hits"]["hits"]))
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

                # print(hit_dict)
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
                                               "last_seconds": last_seconds,
                                               "topn_search": topn_search
                                               })


class IndexView(View):
    @staticmethod
    def get(request):
        # 热门搜索
        topn_search_clean = []
        topn_search = redis_cli.zrevrangebyscore(
            "search_keywords_set", "+inf", "-inf", start=0, num=5)
        for topn_key in topn_search:
            topn_key = str(topn_key, encoding="utf-8")
            topn_search_clean.append(topn_key)
        topn_search = topn_search_clean

        # print(queryList[0])
        return render(request, "index.html", {"topn_search": topn_search})


class DetailView(View):
    def get(self, request):
        id = request.GET.get("id", "")
        doc = Document.get(id=id, index='policynew', using=client).to_dict()
        link = doc['link']
        title = doc['title']

        policy_object_list = []
        # 从数据库中取出推荐的政策
        policy_recommend = PolicyRecommend.objects.filter(title=title)
        if len(policy_recommend) > 0:
            policy_object = policy_recommend[0]
            policy_str = policy_object.recommend
            policy_items = policy_str.split(",")[:3]
            policy_names = [item.split(' ')[0] for item in policy_items]
            policy_scores = [item.split(' ')[1] for item in policy_items if len(item.split(' ')[1]) == 7]
            print(policy_scores)
            policy_recommend_urls = []
            for policy_name in policy_names:
                resp = Search(using=client, index='policynew').query("match", title=policy_name)
                response = resp.execute()
                link_str = response['hits']['hits'][0]["_id"]
                if (policy_name == response[0].title):
                    policy_recommend_url = "http://127.0.0.1:8000/detail/?id=" + link_str
                else:
                    policy_recommend_url = ""
                policy_recommend_urls.append(policy_recommend_url)
            policy_object_list = list(zip(policy_names, policy_scores, policy_recommend_urls))
            # relation_policies_dict[relation_policy] = relation_policy_url

        # 从数据库中取出相关的政策
        relation_policies_dict = {}
        relations = RelationPolicies.objects.filter(title=title)
        if len(relations) == 1:
            # print(relations[0].relation_policies)
            relation_policies = set(relations[0].relation_policies.split(','))
            # print(relation_policies)
            for relation_policy in relation_policies:
                if (relation_policy != ''):
                    resp = Search(using=client, index='policynew').query("match", title=relation_policy)
                    response = resp.execute()
                    link_str = response['hits']['hits'][0]["_id"]
                    if (relation_policy == response[0].title):
                        relation_policy_url = "http://127.0.0.1:8000/detail/?id=" + link_str
                    else:
                        relation_policy_url = ""
                    relation_policies_dict[relation_policy] = relation_policy_url

        # 生成结果返回对象
        result_dict = {}
        result_dict['link'] = link
        if policy_object_list != []:
            print(policy_object_list)
            result_dict['policy_object_list'] = policy_object_list
        if relation_policies_dict != {}:
            result_dict['relation_policies_dict'] = relation_policies_dict
        return render(request, 'detail.html', {'link': link, 'relation_policies_dict': relation_policies_dict,
                                               'policy_object_list': policy_object_list})


class SearchSuggest(View):
    '''搜索补全(搜索建议)'''

    @staticmethod
    def get(request):
        key_words = request.GET.get('s')
        suggest_list = []
        if key_words:
            s = PolicyType.search()
            """fuzzy模糊搜索, fuzziness 编辑距离, prefix_length前面不变化的前缀长度"""
            s = s.suggest('my_suggest', key_words, completion={
                "field": "suggest",
                "fuzzy": {
                    "fuzziness": 0
                },
                "size": 10
            })
            suggestions = s.execute()
            for match in suggestions.suggest.my_suggest[0].options[:10]:
                source = match._source
                suggest_list.append(source["title"])
        return HttpResponse(
            json.dumps(suggest_list), content_type="application/json")


'''从一张表中查询，每次收到请求更新表'''


class HotArticle(View):
    @classmethod
    def update_table(cls):
        query_set = SearchDetailRecord.objects.values("title").annotate(total=Count('id')).order_by('-total')[:5]
        print(query_set.query)
        for index, query_item in enumerate(query_set):
            article = Hotarticle()
            article.id = index + 1
            article.title = query_item['title']
            article.save()

    def get(self, request):
        t = threading.Thread(target=self.update_table, name="UpdateTable")
        t.start()
        hotarticle_dict = {}
        query_set = Hotarticle.objects.all()
        for index, query_item in enumerate(query_set):
            hotarticle_dict[index] = query_item.title
            # print(query_item.title)
        return HttpResponse(json.dumps(hotarticle_dict, ensure_ascii=False), content_type='application/json')
