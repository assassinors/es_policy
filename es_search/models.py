from django.db import models
from elasticsearch_dsl import Document,Long,Keyword,Text,Date
# Create your models here.
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