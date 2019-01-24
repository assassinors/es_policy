from django.test import TestCase

# Create your tests here.
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import Document,Text,Keyword,Date,Integer
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

class Article(Document):
    title = Text(analyzer='snowball',fields={'raw':Keyword()})
    body = Text(analyzer='snowball')
    tags = Keyword()
    publish_from = Date()
    lines = Integer()

    class Index():
        name = 'blog',
        doc_type = '_nihao',
        settings = {
            "number_of_shards" : 1,
        }
    class Meta():
        doc_type = 'nihao'

    def save(self,**kwargs):
        self.lines = len(self.body.split())
        return super(Article,self).save(**kwargs)
    def is_published(self):
        return datetime.now() >= self.publish_from


Article.init()

# article = Article(meta={'id':42},title='Hello World',tags=['test'])
# article.body = '''loong text'''
# article.published_from = datetime.now()
# article.save()

# article = Article.get(id=42)
# print(article.is_published())




