from django.db import models
from elasticsearch_dsl import Document, Long, Keyword, Text, Date, Index, Completion
from elasticsearch_dsl import analyzer
from elasticsearch_dsl.connections import connections

# Create your models here.

connections.create_connection(hosts=['10.1.62.240'])
my_analyzer = analyzer('ik_smart')


class PolicyData(models.Model):
    link = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    data_id = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    dispatch_number = models.CharField(max_length=255, blank=True, null=True)
    file_paths = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'policy_data'
        unique_together = (('id', 'title'),)


class RelationPolicies(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    relation_policies = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'relation_policies'


class SearchRecord(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=100)  # Field name made lowercase.
    os = models.TextField(db_column='OS', blank=True, null=True)  # Field name made lowercase.
    browser = models.TextField(db_column='BROWSER', blank=True, null=True)  # Field name made lowercase.
    ip = models.CharField(db_column='IP', max_length=100, blank=True, null=True)  # Field name made lowercase.
    remote_port = models.CharField(db_column='REMOTE_PORT', max_length=100, blank=True,
                                   null=True)  # Field name made lowercase.
    channel = models.CharField(db_column='CHANNEL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    result_count = models.TextField(db_column='RESULT_COUNT', blank=True, null=True)  # Field name made lowercase.
    session_id = models.TextField(db_column='SESSION_ID', blank=True, null=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='USER_ID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    user_name = models.CharField(db_column='USER_NAME', max_length=100, blank=True,
                                 null=True)  # Field name made lowercase.
    search_date = models.CharField(db_column='SEARCH_DATE', max_length=100, blank=True,
                                   null=True)  # Field name made lowercase.
    search_time = models.CharField(db_column='SEARCH_TIME', max_length=100, blank=True,
                                   null=True)  # Field name made lowercase.
    extend_1 = models.TextField(db_column='EXTEND_1', blank=True, null=True)  # Field name made lowercase.
    extend_2 = models.TextField(db_column='EXTEND_2', blank=True, null=True)  # Field name made lowercase.
    extend_3 = models.TextField(db_column='EXTEND_3', blank=True, null=True)  # Field name made lowercase.
    keyword = models.TextField(db_column='KEYWORD', blank=True, null=True)  # Field name made lowercase.
    query_time = models.TextField(db_column='QUERY_TIME', blank=True, null=True)  # Field name made lowercase.
    ip_area = models.CharField(db_column='IP_AREA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ip_num = models.TextField(db_column='IP_NUM', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SEARCH_RECORD'


class SearchDetailRecord(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=50)  # Field name made lowercase.
    url = models.TextField(db_column='URL', blank=True, null=True)  # Field name made lowercase.
    keyword = models.TextField(db_column='KEYWORD', blank=True, null=True)  # Field name made lowercase.
    channel = models.CharField(db_column='CHANNEL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    title = models.TextField(db_column='TITLE', blank=True, null=True)  # Field name made lowercase.
    logo = models.TextField(db_column='LOGO', blank=True, null=True)  # Field name made lowercase.
    page_index = models.DecimalField(db_column='PAGE_INDEX', max_digits=65, decimal_places=30, blank=True, null=True)
    page_no = models.DecimalField(db_column='PAGE_NO', max_digits=65, decimal_places=30, blank=True, null=True)
    user_ip = models.CharField(db_column='USER_IP', max_length=100, blank=True, null=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='USER_ID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    user_name = models.CharField(db_column='USER_NAME', max_length=100, blank=True,
                                 null=True)  # Field name made lowercase.
    search_detail_time = models.DateTimeField(db_column='SEARCH_DETAIL_TIME', blank=True,
                                              null=True)  # Field name made lowercase.
    search_detail_stamp = models.DecimalField(db_column='SEARCH_DETAIL_STAMP', max_digits=65, decimal_places=30,
                                              blank=True, null=True)
    # Field name made lowercase.
    anchor = models.CharField(db_column='ANCHOR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    source_id = models.CharField(db_column='SOURCE_ID', max_length=200, blank=True,
                                 null=True)  # Field name made lowercase.
    session_id = models.CharField(db_column='SESSION_ID', max_length=200, blank=True,
                                  null=True)  # Field name made lowercase.
    item_unique_coding = models.CharField(db_column='ITEM_UNIQUE_CODING', max_length=200, blank=True, null=True)
    user_ip_area = models.CharField(db_column='USER_IP_AREA', max_length=255, blank=True,
                                    null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SEARCH_DETAIL_RECORD'


class PolicyRecommend(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    recommend = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'policy_recommend'


class PolicyType(Document):
    suggest = Completion(analyzer=my_analyzer)
    link = Keyword()
    title = Text(analyzer="ik_max_word")
    data_id = Keyword()
    category = Text(analyzer="ik_max_word")
    organization = Keyword()
    create_date = Date()
    dispatch_number = Keyword()
    content = Text(analyzer="ik_max_word")

    class Index:
        name = 'policynew',
        settings = {
            'number_of_replicas': 0
        }
