from django.db import models
from simplepro.editor import fields
from simplepro.lib import pkHelper


class BaseModel(models.Model):
    id = models.CharField(max_length=48, primary_key=True, editable=False, default=pkHelper.uuid_generator)
    createdAt = models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name="创建时间", null=True,
                                     editable=False, db_index=True)
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="最近更新时间", null=True, editable=False, db_index=True)
    deletedAt = models.DateTimeField(verbose_name="被删除时间", null=True, editable=False, db_index=True)
    remark = models.CharField(verbose_name="小备注/标签", max_length=100, null=True, blank=True, db_index=True)
    info = fields.UETextField(verbose_name='说明', null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['-updatedAt']


class BaseModelWithShowRate(BaseModel):
    showTimes = models.IntegerField(verbose_name="被观看次数", default=0, editable=False)

    def show(self):
        self.showTimes += 1
        self.save()

    class Meta:
        abstract = True
