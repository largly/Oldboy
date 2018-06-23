from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

import hashlib
import datetime


# ############ 1. 课程相关 #############
class CourseCategory(models.Model):
    """课程大类, e.g 前端  后端..."""
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = "课程大类"
        verbose_name_plural = "课程大类"


class CourseSubCategory(models.Model):
    """课程子类, e.g python linux """
    category = models.ForeignKey("CourseCategory")
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = "课程子类"
        verbose_name_plural = "课程子类"


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


class Scholarship(models.Model):
    """学位课程奖学金，例如：使用20%的时间学完课程，则奖励5000；使用50%的时间学完课程，则奖励2000"""
    degree_course = models.ForeignKey("DegreeCourse")
    time_percent = models.PositiveSmallIntegerField(verbose_name="奖励档位(时间百分比)", help_text="只填百分值，如80,代表80%")
    value = models.PositiveIntegerField(verbose_name="奖学金数额")


class Course(models.Model):
    """普通课程或学位课的模块"""
    name = models.CharField(max_length=128, unique=True, verbose_name='课程名称或学位课模块名称')
    course_img = models.CharField(max_length=255, verbose_name='课程图片')
    sub_category = models.ForeignKey("CourseSubCategory", verbose_name='课程所属类')


    course_type_choices = ((1, '付费'), (2, 'VIP专享'), (3, '学位课程'))
    course_type = models.SmallIntegerField(choices=course_type_choices)

    # 和学位课做FK，可以为  blank=True, null=True,
    degree_course = models.ForeignKey("DegreeCourse", blank=True, null=True, help_text="若是学位课程的模块，此处关联学位表")


    brief = models.TextField(verbose_name="课程概述", max_length=2048)
    level_choices = ((1, '初级'), (2, '中级'), (3, '高级'))
    level = models.SmallIntegerField(choices=level_choices, default=1)
    pub_date = models.DateField(verbose_name="发布日期", blank=True, null=True)
    period = models.PositiveIntegerField(verbose_name="建议学习周期(days)", default=7)
    order = models.IntegerField("课程顺序", help_text="从上一个课程数字往后排")
    attachment_path = models.CharField(max_length=128, verbose_name="课件路径", blank=True, null=True)
    status_choices = ((1, '上线'), (2, '下线'), (3, '预上线'))
    status = models.SmallIntegerField(choices=status_choices, default=1)

    # 用于GenericForeignKey反向查询，不会生成表字段，切勿删除
    # coupon = GenericRelation("Coupon")
    # 用于GenericForeignKey反向查询，不会生成表字段，切勿删除
    price_policy = GenericRelation("PricePolicy")


    def save(self, *args, **kwargs):
        if self.course_type == 3:
            if not self.degree_course:
                raise ValueError("学位课程必须关联对应的学位表")
        super(Course, self).save(*args, **kwargs)


class CourseDetail(models.Model):
    """课程详情页内容"""
    course = models.OneToOneField("Course")
    hours = models.IntegerField("课时")
    course_slogan = models.CharField(max_length=125, blank=True, null=True, verbose_name='课程Slogan')
    video_brief_link = models.CharField(verbose_name='课程介绍', max_length=255, blank=True, null=True)
    why_study = models.TextField(verbose_name="为什么学习这门课程")
    what_to_study_brief = models.TextField(verbose_name="我将学到哪些内容")
    career_improvement = models.TextField(verbose_name="此项目如何有助于我的职业生涯")
    prerequisite = models.TextField(verbose_name="课程先修要求", max_length=1024)
    teachers = models.ManyToManyField("Teacher", verbose_name="课程讲师")
    recommend_courses = models.ManyToManyField('Course', verbose_name="推荐课程", related_name="recommend_by")


class OftenAskedQuestion(models.Model):
    """课程和学位课的常见问题"""

    content_type = models.ForeignKey(ContentType, verbose_name='关联课程或学位课程表')
    object_id = models.PositiveIntegerField(verbose_name='关联课程或学位课程表中的课程ID')
    content_object = GenericForeignKey('content_type', 'object_id')
    question = models.CharField(max_length=255, verbose_name='问题')
    answer = models.TextField(max_length=1024, verbose_name='回答')

    class Meta:
        unique_together = ('content_type', 'object_id', 'question')


class CourseOutline(models.Model):
    """课程大纲"""
    course_detail = models.ForeignKey("CourseDetail")
    title = models.CharField(max_length=128, verbose_name='大纲标题')
    content = models.TextField(max_length=1024, verbose_name='大纲内容')
    order = models.PositiveSmallIntegerField(default=1, verbose_name='大纲显示顺序')

    class Meta:
        unique_together = ('course_detail', 'title')


class CourseChapter(models.Model):
    """课程章节"""
    course = models.ForeignKey("Course", related_name='course_chapters')
    chapter = models.SmallIntegerField(verbose_name="章节序号（第N章）", default=1)
    name = models.CharField(max_length=128, verbose_name='章节名称')
    summary = models.TextField(verbose_name="章节介绍", blank=True, null=True)
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)

    class Meta:
        unique_together = ("course", 'chapter')

    def __str__(self):
        return self.name

class CourseSection(models.Model):
    """课时"""
    chapter = models.ForeignKey("CourseChapter", related_name='course_sections')
    name = models.CharField(max_length=128, verbose_name='课程名称')
    section_type_choices = ((1, '文档'), (2, '练习'), (3, '视频'))
    section_type = models.SmallIntegerField(default=3, choices=section_type_choices, verbose_name='课程类型')

    order = models.PositiveSmallIntegerField(verbose_name="课时顺序", help_text="建议每个课时之间空1至2个值，以备后续插入课时")
    section_link = models.CharField(verbose_name='课时链接', max_length=255, blank=True, null=True,
                                    help_text="若是video，填CC视频的唯一标识（如：ECC9954677D8E1079C33DC5901307461）,若是文档或练习，填链接")
    video_time = models.CharField(verbose_name="视频时长(在前端显示)", blank=True, null=True, max_length=32)
    pub_date = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    free_trail = models.BooleanField("是否可试看", default=False)

    class Meta:
        unique_together = ('chapter', 'section_link')

    def  __str__(self):
        return  self.name
class Homework(models.Model):
    """课程章节作业和考核"""
    chapter = models.ForeignKey("CourseChapter")
    title = models.CharField(max_length=128, verbose_name="作业题目")
    order = models.PositiveSmallIntegerField("作业顺序", help_text="同一课程的每个作业之前的order值间隔1-2个数")
    homework_type_choices = ((1, '作业'), (2, '模块通关考核'))
    homework_type = models.SmallIntegerField(choices=homework_type_choices, default=1)
    requirement = models.TextField(max_length=1024, verbose_name="作业需求")
    threshold = models.TextField(max_length=1024, verbose_name="踩分点")
    recommend_period = models.PositiveSmallIntegerField("推荐完成周期(天)", default=7, help_text='用于计算奖学金')
    scholarship_value = models.PositiveSmallIntegerField("为该作业分配的奖学金(贝里)")
    enabled = models.BooleanField(default=True, help_text="本作业如果后期不需要了，不想让学员看到，可以设置为False")
    note = models.TextField(blank=True, null=True, verbose_name='注意事项')

    class Meta:
        unique_together = ("chapter", "title")


class PricePolicy(models.Model):
    """价格与有课程效期表"""
    content_type = models.ForeignKey(ContentType, verbose_name='关联普通课或者学位课表',related_name='content_types')
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

    class Meta:
        unique_together = ("content_type", 'object_id', "valid_period")




# ############ 2. 账户相关 #############

class Account(models.Model):
    """用户账户"""
    username = models.CharField("用户名", max_length=64, unique=True)
    email = models.EmailField(verbose_name='邮箱', max_length=255, unique=True, blank=True, null=True)
    password = models.CharField(verbose_name='密码', max_length=128)


class UserAuthToken(models.Model):
    """
    用户Token表
    """
    user = models.OneToOneField(to="Account")
    token = models.CharField(max_length=40, unique=True)
    created = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.token = self.generate_key()
        self.created = datetime.datetime.utcnow()
        return super(UserAuthToken, self).save(*args, **kwargs)

    def generate_key(self):
        """根据用户名和时间生成唯一标识"""
        username = self.user.username
        now = str(datetime.datetime.now()).encode('utf-8')
        md5 = hashlib.md5(username.encode('utf-8'))
        md5.update(now)
        return md5.hexdigest()


# ############ 5. 深科技 #############
class ArticleSource(models.Model):
    """文章来源"""
    name = models.CharField(max_length=64, unique=True)


class Article(models.Model):
    """文章资讯"""
    title = models.CharField(max_length=255, unique=True, db_index=True, verbose_name="文章标题")
    source = models.ForeignKey("ArticleSource", verbose_name="来源")
    article_type_choices = ((1, '资讯'), (2, '视频'))
    article_type = models.SmallIntegerField(choices=article_type_choices, default=1)
    brief = models.TextField(max_length=512, verbose_name="摘要")
    head_img = models.CharField(max_length=255, verbose_name='文章图片')
    content = models.TextField(verbose_name="文章正文")

    pub_date = models.DateTimeField(verbose_name="上架日期")
    offline_date = models.DateTimeField(verbose_name="下架日期")
    status_choices = ((1, '在线'), (2, '下线'))
    status = models.SmallIntegerField(choices=status_choices, default=1, verbose_name="状态")
    order = models.SmallIntegerField(default=0, verbose_name="权重", help_text="文章想置顶，可以把数字调大，不要超过1000")

    vid = models.CharField(max_length=128, verbose_name="视频VID", help_text="文章类型是视频, 则需要添加视频VID", blank=True, null=True)
    comment_num = models.SmallIntegerField(default=0, verbose_name="评论数")
    agree_num = models.SmallIntegerField(default=0, verbose_name="点赞数")
    view_num = models.SmallIntegerField(default=0, verbose_name="观看数")
    collect_num = models.SmallIntegerField(default=0, verbose_name="收藏数")

    # tags = models.ManyToManyField("Tags", blank=True, verbose_name="标签")
    date = models.DateTimeField(auto_now_add=True, verbose_name="创建日期")

    position_choices = ((1, '信息流'), (2, 'banner大图'), (3, 'banner小图'))
    position = models.SmallIntegerField(choices=position_choices, default=1, verbose_name="位置")
    comment = GenericRelation("Comment", help_text='用于GenericForeignKey反向查询,不会生成表字段，切勿删除')


class Collection(models.Model):
    """收藏"""
    account = models.ForeignKey("Account", verbose_name='用户')

    content_type = models.ForeignKey(ContentType, verbose_name='文章或视频表')
    object_id = models.PositiveIntegerField(verbose_name='文章或者视频ID')
    content_object = GenericForeignKey('content_type', 'object_id')

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('content_type', 'object_id', 'account')


class Comment(models.Model):
    """通用的评论表"""
    account = models.ForeignKey("Account", verbose_name="用户")

    content_type = models.ForeignKey(ContentType, blank=True, null=True, verbose_name="文章或视频表")
    object_id = models.PositiveIntegerField(blank=True, null=True, verbose_name='文章或者视频ID')
    content_object = GenericForeignKey('content_type', 'object_id')

    p_node = models.ForeignKey("self", blank=True, null=True, verbose_name="父级评论")
    content = models.TextField(max_length=1024)

    disagree_number = models.IntegerField(default=0, verbose_name="踩")
    agree_number = models.IntegerField(default=0, verbose_name="赞同数")
    date = models.DateTimeField(auto_now_add=True)


# ############ 3. 购买和课程服务相关 #############
class Coupon(models.Model):
    """优惠券生成规则"""
    name = models.CharField(max_length=64, verbose_name="活动名称")
    brief = models.TextField(verbose_name="优惠券介绍")

    coupon_type_choices = ((1, '通用券'), (2, '满减券'), (3, '折扣券'))
    coupon_type = models.SmallIntegerField(choices=coupon_type_choices, default=1, verbose_name="券类型")

    money_equivalent_value = models.IntegerField(verbose_name="等值货币（通用和满减券时可抵扣的钱）", default=0)
    off_percent = models.PositiveSmallIntegerField("折扣百分比", help_text="只针对折扣券，例7.9折，写79", blank=True, null=True)
    minimum_consume = models.PositiveIntegerField("最低消费", default=0, help_text="仅在满减券时填写此字段")

    content_type = models.ForeignKey(ContentType, blank=True, null=True, verbose_name='优惠券关联的表（普通课程）')
    object_id = models.PositiveIntegerField(verbose_name="绑定课程", blank=True, null=True, help_text="可以把优惠券跟课程ID绑定")
    content_object = GenericForeignKey('content_type', 'object_id')

    quantity = models.PositiveIntegerField("数量(张)", default=1)

    open_date = models.DateField("优惠券领取开始时间")
    close_date = models.DateField("优惠券领取结束时间")
    valid_begin_date = models.DateField(verbose_name="有效期开始时间", blank=True, null=True)
    valid_end_date = models.DateField(verbose_name="有效结束时间", blank=True, null=True)
    coupon_valid_days = models.PositiveIntegerField(verbose_name="优惠券有效期（天）", blank=True, null=True,
                                                    help_text="自券被领时开始算起")

    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.coupon_valid_days or (self.valid_begin_date and self.valid_end_date):
            if self.valid_begin_date and self.valid_end_date:
                if self.valid_end_date <= self.valid_begin_date:
                    raise ValueError("valid_end_date 有效期结束日期必须晚于 valid_begin_date ")
            if self.coupon_valid_days == 0:
                raise ValueError("coupon_valid_days 有效期不能为0")
        if self.close_date < self.open_date:
            raise ValueError("close_date 优惠券领取结束时间必须晚于 open_date优惠券领取开始时间 ")

        super(Coupon, self).save(*args, **kwargs)


class CouponRecord(models.Model):
    """优惠券发放、消费纪录"""
    coupon = models.ForeignKey("Coupon")
    account = models.ForeignKey("Account", verbose_name="拥有者")
    number = models.CharField(max_length=64, unique=True, verbose_name='优惠券唯一标识')
    status_choices = ((1, '未使用'), (2, '已使用'), (3, '已过期'))
    status = models.SmallIntegerField(choices=status_choices, default=1)

    get_time = models.DateTimeField(verbose_name="领取时间", help_text="用户领取时间")
    used_time = models.DateTimeField(blank=True, null=True, verbose_name="使用时间")
    date = models.DateTimeField(auto_now_add=True, verbose_name="生成时间")

    order = models.ForeignKey("Order", blank=True, null=True, verbose_name="关联订单（订单使用优惠券）")


class TransactionRecord(models.Model):
    """贝里交易纪录"""
    account = models.ForeignKey("Account")
    amount = models.IntegerField("金额")
    balance = models.IntegerField("账户余额")
    transaction_type_choices = ((0, '收入'), (1, '支出'), (2, '退款'), (3, "提现"))  # 2 为了处理 订单过期未支付时，锁定期贝里的回退
    transaction_type = models.SmallIntegerField(choices=transaction_type_choices)

    content_type = models.ForeignKey(ContentType, blank=True, null=True, verbose_name='关联表，如：订单表、奖惩表')
    object_id = models.PositiveIntegerField(blank=True, null=True, verbose_name="关联对象，如：某个订单ID、某项奖惩ID")
    content_object = GenericForeignKey('content_type', 'object_id')

    transaction_number = models.CharField(unique=True, verbose_name="流水号（为每一笔生成贝里交易生成唯一标识）", max_length=128)
    date = models.DateTimeField(auto_now_add=True)
    memo = models.CharField(max_length=128, blank=True, null=True)


class Order(models.Model):
    """订单"""
    account = models.ForeignKey("Account")
    order_number = models.CharField(max_length=128, verbose_name="订单唯一标识（自动生成）", unique=True)
    payment_type_choices = ((1, '微信'), (2, '支付宝'), (3, '优惠码'), (4, '贝里'))
    payment_type = models.SmallIntegerField(choices=payment_type_choices)
    actual_amount = models.FloatField(verbose_name="实付金额")
    payment_number = models.CharField(max_length=128, verbose_name="支付第3方订单号", null=True, blank=True)

    status_choices = ((1, '交易成功'), (2, '待支付'), (3, '退费申请中'), (4, '已退费'), (5, '主动取消'), (6, '超时取消'))
    status = models.SmallIntegerField(choices=status_choices, verbose_name="状态")

    date = models.DateTimeField(auto_now_add=True, verbose_name="订单生成时间")
    pay_time = models.DateTimeField(blank=True, null=True, verbose_name="付款时间")
    cancel_time = models.DateTimeField(blank=True, null=True, verbose_name="订单取消时间")


class OrderDetail(models.Model):
    """订单详情"""
    order = models.ForeignKey("Order")

    content_type = models.ForeignKey(ContentType, verbose_name='关联课程或学位课程表')
    object_id = models.PositiveIntegerField(verbose_name='关联课程或学位课程表中的课程ID')
    content_object = GenericForeignKey('content_type', 'object_id')

    original_price = models.FloatField("课程原价")
    price = models.FloatField("折后价格")

    valid_period_display = models.CharField("有效期显示", max_length=32, help_text='用于页面上显示')
    valid_period = models.PositiveIntegerField("有效期(days)", help_text='用于计算课程有效期')
    memo = models.CharField(max_length=255, blank=True, null=True, verbose_name='其他说明')

    class Meta:
        unique_together = ("order", 'content_type', 'object_id')


class EnrolledCourse(models.Model):
    """已报名不同课程,不包括学位课程"""
    order_detail = models.OneToOneField("OrderDetail", verbose_name='关联订单详细')
    account = models.ForeignKey("Account")
    course = models.ForeignKey("Course")

    enrolled_date = models.DateTimeField(auto_now_add=True, verbose_name='购买课程时间')
    valid_begin_date = models.DateField(verbose_name="有效期开始自")
    valid_end_date = models.DateField(verbose_name="有效期结束至")

    status_choices = ((1, '已开通'), (2, '已过期'))
    status = models.SmallIntegerField(choices=status_choices, default=1)


class EnrolledDegreeCourse(models.Model):
    """已报名的学位课程"""
    order_detail = models.OneToOneField("OrderDetail", verbose_name='关联订单详细')

    account = models.ForeignKey("Account")
    degree_course = models.ForeignKey("DegreeCourse")
    enrolled_date = models.DateTimeField(auto_now_add=True, verbose_name='购买课程时间')
    valid_begin_date = models.DateField(verbose_name="有效期开始自", blank=True, null=True, help_text='开通模块时再设置有效期')
    valid_end_date = models.DateField(verbose_name="有效期结束至", blank=True, null=True)
    status_choices = (
        (1, '在学中'),
        (2, '休学中'),
        (3, '已毕业'),
        (4, '超时结业'),
        (5, '未开始'),
    )
    study_status = models.SmallIntegerField(choices=status_choices, default=5)
    mentor = models.ForeignKey("Account", verbose_name="导师", related_name='my_students', blank=True, null=True)
    mentor_fee_balance = models.PositiveIntegerField("导师费用余额", help_text="这个学员的导师费用，每有惩罚，需在此字段同时扣除")

    class Meta:
        unique_together = ('account', 'degree_course')


class DegreeRegistrationForm(models.Model):
    """学位课程报名表"""
    enrolled_degree = models.OneToOneField("EnrolledDegreeCourse")
    current_company = models.CharField(max_length=64, verbose_name='公司')
    current_position = models.CharField(max_length=64, verbose_name='职位')
    current_salary = models.IntegerField(verbose_name='薪资')
    work_experience_choices = (
        (1, "应届生"),
        (2, "1年"),
        (3, "2年"),
        (4, "3年"),
        (5, "4年"),
        (6, "5年"),
        (7, "6年"),
        (8, "7年"),
        (9, "8年"),
        (10, "9年"),
        (11, "10年"),
        (12, "超过10年"),
    )
    work_experience = models.IntegerField(verbose_name='工作经验')
    open_module = models.BooleanField(verbose_name="是否开通第1模块", default=True)
    stu_specified_mentor = models.CharField(verbose_name="学员自行指定的导师名", max_length=32, blank=True, null=True)
    study_plan_choices = (
        (1, "1-2小时/天"),
        (2, "2-3小时/天"),
        (3, "3-5小时/天"),
        (4, "5小时+/天"),
    )
    study_plan = models.SmallIntegerField(choices=study_plan_choices, default=1)
    why_take_this_course = models.TextField(verbose_name="报此课程原因", max_length=1024)
    why_choose_us = models.TextField(verbose_name="为何选路飞", max_length=1024)
    your_expectation = models.TextField(verbose_name="你的期待", max_length=1024)


class StudyRecord(models.Model):
    """学位课程的模块学习进度，报名学位课程后，每个模块会立刻生成一条学习纪录"""
    enrolled_degree_course = models.ForeignKey("EnrolledDegreeCourse")
    course_module = models.ForeignKey("Course", verbose_name="学位模块")
    open_date = models.DateField(blank=True, null=True, verbose_name="开通日期")
    end_date = models.DateField(blank=True, null=True, verbose_name="完成日期")
    status_choices = ((1, '在学'), (2, '未开通'), (3, '已完成'))
    status = models.SmallIntegerField(choices=status_choices, default=1, verbose_name="状态")

    class Meta:
        unique_together = ('enrolled_degree_course', 'course_module')

    def save(self, *args, **kwargs):
        if self.course_module.degree_course_id != self.enrolled_degree_course.degree_course_id:
            raise ValueError("学员要开通的模块必须与其报名的学位课程一致！")

        super(StudyRecord, self).save(*args, **kwargs)


class HomeworkRecord(models.Model):
    """学员作业记录及成绩"""
    homework = models.ForeignKey("Homework")
    student = models.ForeignKey("EnrolledDegreeCourse", verbose_name="学生")
    score_choices = (
        (100, 'A+'),
        (90, 'A'),
        (85, 'B+'),
        (80, 'B'),
        (70, 'B-'),
        (60, 'C+'),
        (50, 'C'),
        (40, 'C-'),
        (-1, 'D'),
        (0, 'N/A'),
        (-100, 'COPY'),
    )
    score = models.SmallIntegerField(verbose_name="分数", choices=score_choices, null=True, blank=True)
    mentor = models.ForeignKey("Account", related_name="my_stu_homework_record", limit_choices_to={'role': 1},
                               verbose_name="导师")
    mentor_comment = models.TextField(verbose_name="导师批注", blank=True, null=True)
    status_choice = (
        (1, '待批改'),
        (2, '已通过'),
        (3, '不合格'),
    )
    status = models.SmallIntegerField(verbose_name='作业状态', choices=status_choice, default=1)

    submit_num = models.SmallIntegerField(verbose_name='提交次数', default=0)
    correct_date = models.DateTimeField('备注日期', blank=True, null=True)

    date = models.DateTimeField("作业提交日期", auto_now_add=True)
    check_date = models.DateTimeField("批改日期", null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name="提交日期")
    reward_choice = (
        (1, '新提交'),
        (2, '按时提交'),
        (3, '未按时提交'),
        (4, '成绩已奖励'),
        (5, '成绩已处罚'),
        (6, '未作按时检测'),
    )
    reward_status = models.SmallIntegerField(verbose_name='作业记录奖惩状态', default=1)

    class Meta:
        unique_together = ("homework", "student")


class StuFollowUpRecord(models.Model):
    """学员跟进记录"""
    enrolled_degree_course = models.ForeignKey("EnrolledDegreeCourse", verbose_name="学生")
    mentor = models.ForeignKey("Account", related_name='mentor', limit_choices_to={'role': 1}, verbose_name="导师")
    followup_tool_choices = ((1, 'QQ'), (2, '微信'), (3, '电话'), (4, '系统通知'))
    followup_tool = models.SmallIntegerField(choices=followup_tool_choices, default=1)
    record = models.TextField(verbose_name="跟进记录")
    attachment_path = models.CharField(max_length=128, blank=True, null=True, verbose_name="附件路径", help_text="跟进记录的截图等")
    date = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    """课程提问"""
    name = models.CharField(max_length=128, verbose_name="问题概要", db_index=True)
    question_type_choices = ((1, '专题课程问题'), (2, '学位课程问题'))
    question_type = models.SmallIntegerField(choices=question_type_choices, default=1, verbose_name="来源")
    account = models.ForeignKey("Account", verbose_name="提问者")
    degree_course = models.ForeignKey("DegreeCourse", blank=True, null=True, help_text='若是针对整个学位课程的提问，关联这个')
    course_section = models.ForeignKey("CourseSection", blank=True, null=True, help_text='针对整个学位课程的提问不需关联特定课时')
    content = models.TextField(max_length=1024, verbose_name="问题内容")
    enquiries_count = models.IntegerField(default=0, verbose_name="同问者计数")
    attachment_path = models.CharField(max_length=128, blank=True, null=True, verbose_name="附件路径", help_text="问题记录的截图等")
    date = models.DateTimeField(auto_now_add=True)
    status_choices = ((0, '待解答'), (1, '已解答'), (2, '已关闭'))
    status = models.SmallIntegerField(choices=status_choices, default=0)

    def save(self, *args, **kwargs):
        if self.degree_course is None and self.course_section is None:
            raise ValueError("提的问题必须关联学位课程或具体课时！")

        super(Question, self).save(*args, **kwargs)


class Answer(models.Model):
    """问题解答"""
    question = models.ForeignKey("Question", verbose_name="问题")
    content = models.TextField(verbose_name="回答")
    account = models.ForeignKey("Account", verbose_name="回答者")
    agree_number = models.IntegerField(default=0, verbose_name="点赞数")
    disagree_number = models.IntegerField(default=0, verbose_name="点踩数")
    answer_date = models.DateTimeField(auto_now=True, verbose_name="日期")


class AnswerComment(models.Model):
    """答案回复评论"""
    answer = models.ForeignKey("Answer")
    reply_to = models.ForeignKey("self", blank=True, null=True, verbose_name="基于评论的评论")
    comment = models.TextField(max_length=512, verbose_name="评论内容")
    attachment_path = models.CharField(max_length=128, blank=True, null=True, verbose_name="附件路径", help_text="跟进记录的截图等")
    account = models.ForeignKey("Account", verbose_name="评论者")
    date = models.DateTimeField(auto_now_add=True)


class QACounter(models.Model):
    """ 问题和回答的赞同数量统计 """
    content_type = models.ForeignKey(ContentType, verbose_name='问题或回答表')
    object_id = models.PositiveIntegerField(verbose_name='问题或回答的ID')
    content_object = GenericForeignKey('content_type', 'object_id')

    data_type_choices = ((1, '点赞'), (2, '踩'), (3, '同问'))
    data_type = models.SmallIntegerField(choices=data_type_choices)
    account = models.ForeignKey("Account")
    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("content_type", 'object_id', "account")


# ############ 4. 奖惩规则相关 #############
class ScoreRule(models.Model):
    """积分规则"""
    score_rule_choices = (
        (1, '未按时交作业'),
        (2, '未及时批改作业'),
        (3, '作业成绩'),
        (4, '未在规定时间内对学员进行跟进'),
        (5, '未在规定时间内回复学员问题'),
        (6, '收到学员投诉'),
        (7, '导师相关'),
        (8, '学位奖学金'),
    )
    rule = models.SmallIntegerField(choices=score_rule_choices, verbose_name="积分规则")
    score_type_choices = ((1, '奖励'), (2, '惩罚'), (3, '初始分配'))
    score_type = models.SmallIntegerField(choices=score_type_choices, verbose_name="奖惩")
    score = models.IntegerField(help_text="扣分数与贝里相等")
    memo = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('rule', 'score_type')


class ScoreRecord(models.Model):
    """积分奖惩记录"""
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    degree_course = models.ForeignKey("DegreeCourse", blank=True, null=True, verbose_name="关联学位课程")
    score_rule = models.ForeignKey("ScoreRule", verbose_name="关联规则")
    account = models.ForeignKey("Account", verbose_name="被执行人")

    # 这里单独有一个字段存积分而不是从score_rule里引用的原因是考虑到如果引用的话，
    # 一旦score_rule里的积分有变更，那么所有用户的历史积分也会被影响
    score = models.IntegerField(verbose_name="金额(贝里)")
    balance = models.PositiveIntegerField(verbose_name="奖金余额(贝里)")
    maturity_date = models.DateField("成熟日期(可提现日期)",help_text='每天凌晨定时任务会跑，所以最迟一天')

    applied = models.BooleanField(default=False, help_text="奖赏纪录是否已被执行", verbose_name="是否已被执行")
    applied_date = models.DateTimeField(blank=True, null=True, verbose_name="事件生效日期")
    date = models.DateTimeField(auto_now_add=True, verbose_name="事件触发日期")
