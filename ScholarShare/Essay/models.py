from django.db import models


# Create your models here.
class Author(models.Model):
    is_professional = models.IntegerField('是否认证', default=-1)  # -1未认证，0正在申请，1已认证
    open_alex_id = models.CharField('对应的open_alex_id', max_length=200, db_index=True, default='', null=True)
    real_name = models.CharField('对应的作者真名', max_length=200, db_index=True, default='', null=True)
    institution = models.ForeignKey("Institution", on_delete=models.CASCADE, null=True)

    work_count = models.IntegerField('作者作品数量', default=0)
    # 实体属性
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'Author'


class Work(models.Model):
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    open_alex_id = models.CharField('对应作品的open_alex_id', max_length=200, db_index=True,
                                    default='')
    cited_by_count = models.IntegerField(default=0)
    # yearArr = ArrayField(models.IntegerField(default=0), size=10)
    display_name = models.CharField(max_length=255, null=True)
    doi = models.CharField(max_length=255, null=True)
    language = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)
    venue = models.ForeignKey("Venue", on_delete=models.CASCADE)

    class Meta:
        db_table = 'Works'


class Venue(models.Model):
    open_alex_id = models.CharField('对应Source的open_alex_id', max_length=200, db_index=True,
                                    default='')
    type = models.CharField(max_length=255, null=True)
    # worksYearArr = ArrayField(models.IntegerField(default=0), size=10)
    # citedYearArr = ArrayField(models.IntegerField(default=0), size=10)
    work_count = models.IntegerField(default=0)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'Venue'


class Institution(models.Model):
    open_alex_id = models.CharField('对应机构的open_alex_id', max_length=200, db_index=True,
                                    default='')
    country_code = models.CharField(max_length=200, null=True)
    type = models.CharField(max_length=255, null=True)
    # worksYearArr = ArrayField(models.IntegerField(default=0), size=10)
    # citedYearArr = ArrayField(models.IntegerField(default=0), size=10)
    work_count = models.IntegerField(default=0)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'Institution'


class Concept(models.Model):
    open_alex_id = models.CharField('对应的open_alex_id', max_length=200, db_index=True,
                                    default='')
    cited_by_count = models.IntegerField(default=0)
    # worksYearArr = ArrayField(models.IntegerField(default=0), size=10)
    # citedYearArr = ArrayField(models.IntegerField(default=0), size=10)
    descriptions = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'Concept'


class Year(models.Model):
    year = models.IntegerField(default=0)
    works = models.IntegerField("论文数", default=0)
    cited = models.IntegerField("被引用数", default=0)
    venue = models.ForeignKey("Venue", on_delete=models.CASCADE, null=True)
    work = models.ForeignKey("Work", on_delete=models.CASCADE, null=True)
    concept = models.ForeignKey("Concept", on_delete=models.CASCADE, null=True)
    institution = models.ForeignKey("Institution", on_delete=models.CASCADE, null=True)
