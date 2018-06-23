# from django.urls import reverse
from rest_framework.relations import HyperlinkedRelatedField
from rest_framework.reverse import reverse
from datasource.models import *
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer,SerializerMethodField,HyperlinkedIdentityField,CharField
from rest_framework.throttling import BaseThrottle

class DegreeCourseSerializers(ModelSerializer):
    class Meta:
        model = DegreeCourse
        fields = ['id','name']
        # fields = '__all__'
class DegreeCourseDetaile(HyperlinkedModelSerializer):
    # teachers = HyperlinkedRelatedField(many=True,view_name='teacher-detaile',read_only=True)
    teachers_data = SerializerMethodField()
    prices = SerializerMethodField()

    class Meta:
        model = DegreeCourse
        # fields = '__all__'
        fields = ['url','id','name','course_img','brief','prerequisite','teachers','teachers_data','prices']
        # depth = 2
    def get_teachers_data(self,obj):
        print(self.__dict__)
        temp = [{'id':row.id,'name':row.name,'url':reverse('teacher-detail',request=self._context['request'] ,kwargs={'pk':row.pk})} for row in obj.teachers.all()]
        return temp

    def get_prices(self, obj):

        temp = [{'id': row.id,'price': row.price,'valid_period':row.get_valid_period_display()} for row in obj.degreecourse_price_policy.all()]
        return temp
class CommentSerializers(ModelSerializer):
    account = CharField(source='account.username')
    class Meta:
        model = Comment
        fields = ['id','content','p_node','account']

class CourseSerializers(ModelSerializer):

    # 对于外键，one to one  , choice 可以用这种source方式
    course_type =CharField(source='get_course_type_display')
    class Meta:
        model = Course
        fields = ['id','name','course_type']
        # fields = '__all__'


class CourseDetaileSerializers(HyperlinkedModelSerializer):
    # teachers = HyperlinkedRelatedField(many=True,view_name='teacher-detaile',read_only=True)
    # 对于多对多复杂字段，或者外键取多个字段
    prices = SerializerMethodField()
    question = SerializerMethodField()
    course_detail = SerializerMethodField()
    teachers = SerializerMethodField()
    recommend_courses = SerializerMethodField()
    course_chapter= SerializerMethodField()
    comment = SerializerMethodField()

    class Meta:
        model = Course
        # fields = '__all__'
        fields = ['course_detail','prices','teachers','recommend_courses',
                  'question',
                  'course_chapter',

                  'comment',


                  ]
        # depth = 2
    def get_course_detail(self,obj):
        temp = {'id':obj.coursedetail.id,
                 'hours': obj.coursedetail.hours,
                 'video_brief_link':obj.coursedetail.video_brief_link,
                 'why_study':obj.coursedetail.why_study,
                 'what_to_study_brief':obj.coursedetail.what_to_study_brief,
                 'career_improvement':obj.coursedetail.career_improvement
                 }
        return temp

    def get_teachers(self, obj):

        temp = [{'id': row.id,'name': row.name} for row in obj.coursedetail.teachers.all()]
        return temp

    def get_prices(self, obj):

        temp = [{'id': row.id,'price': row.price,'valid_period':row.get_valid_period_display()} for row in obj.price_policy.all()]
        return temp

    def get_recommend_courses(self, obj):

        temp = [{'id': row.id,'name': row.name} for row in obj.coursedetail.recommend_courses.all()]
        return temp

    def get_question(self,obj):
        question_list = OftenAskedQuestion.objects.filter(content_type__model='course' ,object_id=obj.id)
        temp = [{'id':row.pk, 'question':row.question,'answer':row.answer}   for row in question_list]
        return temp

    def get_course_chapter(self,obj):
        course_chapter_list = CourseChapter.objects.filter(course=obj).all()

        temp = [{chapter_obj.name:[{'id':sections.id,'name':sections.name,'section_link':sections.section_link}
                                   for sections in  chapter_obj.course_sections.all()]}
                for chapter_obj in course_chapter_list]
        return temp

    def get_comment(self,obj):
        comment_list = Comment.objects.filter(content_type__model='coursesection' ,object_id=obj.id)
        temp = [{'id':obj.pk,'content':obj.content,'p_node':obj.p_node_id,'account':obj.account.username} for obj in comment_list]
        return temp


class ArticleSerializers(ModelSerializer):
    source = SerializerMethodField()
    class Meta:
        model = Article
        fields = ['id', 'title', 'source', 'brief', 'head_img', 'comment_num','agree_num','view_num','collect_num']
    def get_source(self,obj):
        return obj.source.name


class ArticleDetailSerializers(HyperlinkedModelSerializer):
    comment = SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id','title','brief','head_img','content', 'comment_num','comment']
    def get_comment(self,obj):
        comment_list = obj.comment.all()
        temp = [{'id':row.id,'content':row.content,'p_node':row.p_node_id,'account':row.account.username,} for row in comment_list]
        return temp


class TeacherSerializers(HyperlinkedModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
        # fields = ['id','name']

class PricePolicySerializers(HyperlinkedModelSerializer):
    class Meta:
        model = PricePolicy
        fields = '__all__'

class ContenttypesSerializers(HyperlinkedModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'


class CollectionSerializers(ModelSerializer):
    content_object = SerializerMethodField()
    class Meta:
        model = Collection
        fields = ['id','content_object']
    def get_content_object(self,obj):
        if obj.content_type.model=='article':
            temp = {'id':obj.content_object.id,'title':obj.content_object.title, 'source':obj.content_object.source.name, 'brief':obj.content_object.brief, 'head_img':obj.content_object.head_img}
        else:
            temp = {'id':obj.content_object.id,'name':obj.content_object.name,'section_link':obj.content_object.section_link}

        return temp