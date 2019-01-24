from django.db import models
from .search import PolicyInfoIndex
from elasticsearch_dsl import Document,Long,Keyword,Text,Date
# Create your models here.
class PolicyIndex(Document):
    id = Long()
    link = Keyword()
    content = Text(analyzer="ik_max_word")
    data_id = Keyword()
    kind = Text(analyzer="ik_max_word")
    organization = Keyword()
    create_date = Date()
    title = Text(analyzer="ik_max_word")
    number = Keyword()
    release_date = Date()
    class Index:
        name = 'policy'
