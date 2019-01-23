from elasticsearch_dsl import connections
from elasticsearch_dsl import DocType,Text,Date,Keyword,Long,Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

connections.create_connection(hosts=['10.1.62.240'])

class PolicyInfoIndex(DocType):
    id = Long()
    link = Keyword()
    content = Text()
    data_id = Keyword()
    kind = Text()
    organization = Keyword()
    create_date = Date()
    title = Text()
    number = Keyword()
    release_date = Date()

    class Index:
        name = 'policy_1'

# PolicyInfoIndex.init()
# 插入数据,从sqlite插入数据到es中
def bulk_indexing():
    PolicyInfoIndex.init() #建立索引
    es = Elasticsearch()
    bulk(client=es,actions=(b.indexing() for b in models.PolicyInfo.objects.all().iterator()))
#     之所以使用iterator()是因为如果数量太多,可以不用一次性加载进内存
#
# def search(organization):
#     s = Search().filter('term',organization=organization)
#     response = s.execute()
#     return response



