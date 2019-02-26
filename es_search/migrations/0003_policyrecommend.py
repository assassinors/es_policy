# Generated by Django 2.1.5 on 2019-02-25 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('es_search', '0002_auto_20190220_1423'),
    ]

    operations = [
        migrations.CreateModel(
            name='PolicyRecommend',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('recommend', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'policy_recommend',
                'managed': False,
            },
        ),
    ]
