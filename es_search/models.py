from django.db import models
from .search import PolicyInfoIndex
# Create your models here.
class PolicyInfo(models.Model): #对应关系数据库中的表
    id = models.IntegerField(primary_key=True)
    link = models.CharField(max_length=100)
    content = models.TextField()
    data_id = models.CharField(max_length=30)
    kind = models.CharField(max_length=50)
    organization = models.CharField(max_length=10)
    create_date = models.DateField()
    title = models.CharField(max_length=50)
    number = models.CharField(max_length=15)
    release_date = models.DateField()

    def indexing(self):  #生成es的文档
        obj = PolicyInfoIndex(  #使用自身数据建立文档
            meta = {'id':self.id},
            link = self.link,
            content = self.content,
            data_id = self.data_id,
            kind = self.kind,
            organization = self.organization,
            create_date = self.create_date,
            title = self.title,
            number = self.number,
            release_date = self.release_date
        )
        obj.save()
        return obj.to_dict(include_meta=True)
