from django.db import models

# Create your models here.


from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class DegreeCourse(models.Model):
    """学位课程"""
    name = models.CharField(max_length=128, unique=True)
    course_img = models.CharField(max_length=255, verbose_name="缩略图")
    brief = models.TextField(verbose_name="学位课程简介", )
    total_scholarship = models.PositiveIntegerField(verbose_name="总奖学金(贝里)", default=40000)
    mentor_compensation_bonus = models.PositiveIntegerField(verbose_name="本课程的导师辅导费用(贝里)", default=15000)
    period = models.PositiveIntegerField(verbose_name="建议学习周期(days)", default=150, help_text='为了计算学位奖学金')
    prerequisite = models.TextField(verbose_name="课程先修要求", max_length=1024)
    teachers = models.ManyToManyField("Teacher", verbose_name="课程讲师")

    # 用于GenericForeignKey反向查询， 不会生成表字段，切勿删除
    # coupon = GenericRelation("Coupon")
    # 用于GenericForeignKey反向查询，不会生成表字段，切勿删除
    degreecourse_price_policy = GenericRelation("PricePolicy")


class Teacher(models.Model):
    """讲师、导师表"""
    name = models.CharField(max_length=32, verbose_name='姓名')
    role_choices = ((1, '讲师'), (2, '导师'))
    role = models.SmallIntegerField(choices=role_choices, default=1)

    title = models.CharField(max_length=64, verbose_name="职位、职称")
    signature = models.CharField(max_length=255, verbose_name="导师签名", blank=True, null=True)
    image = models.CharField(max_length=128, verbose_name='头像')
    brief = models.TextField(max_length=1024, verbose_name='简介')


class PricePolicy(models.Model):
    """价格与有课程效期表"""
    content_type = models.ForeignKey(ContentType, verbose_name='关联普通课或者学位课表',related_name='contents')
    object_id = models.PositiveIntegerField(verbose_name='关联普通课或者学位课中的课程ID')
    content_object = GenericForeignKey('content_type', 'object_id')

    valid_period_choices = (
        (1, '1天'),
        (3, '3天'),
        (7, '1周'),
        (14, '2周'),
        (30, '1个月'),
        (60, '2个月'),
        (90, '3个月'),
        (180, '6个月'),
        (210, '12个月'),
        (540, '18个月'),
        (720, '24个月'),
    )
    valid_period = models.SmallIntegerField(choices=valid_period_choices, verbose_name='课程周期')
    price = models.FloatField(verbose_name='价格')

