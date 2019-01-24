from django.test import TestCase

# Create your tests here.
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import Document,Text,Keyword,Date,Long
from datetime import datetime
from elasticsearch_dsl.connections import connections
# def search(wd):
#     client = Elasticsearch(hosts=[{'host':'10.1.62.240','port':9200}])
#     s = Search(using=client, index='policy').filter('match', content=wd)
#     response = s.execute()
#     for hit in response:
#         print(hit.meta.score,hit.title)
#
# if __name__ == '__main__':
#     wd = '中国'
#     search(wd)

connections.create_connection(hosts=['10.1.62.240'])

class PolicyIndex(Document):
    link = Keyword()
    title = Text(analyzer="ik_max_word")
    data_id = Keyword()
    category = Text(analyzer="ik_max_word")
    organization = Keyword()
    create_date = Date()
    dispatch_number = Keyword()
    content = Text(analyzer="ik_max_word")
    class Index:
        name = 'policydoc',
        settings = {
            'number_of_replicas': 0
        }


PolicyIndex.init()

# article = Article(meta={'id':42},title='Hello World',tags=['test'])
# article.body = '''loong text'''
# article.published_from = datetime.now()
# article.save()

# article = Article.get(id=42)
# print(article.is_published())




