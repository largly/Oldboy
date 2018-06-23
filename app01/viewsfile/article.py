from django_redis import get_redis_connection
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from datasource.models import *
from app01.service.serializerset import *
from rest_framework.parsers import JSONParser
class BaseRespose:

    def __init__(self,error = None,data=None,code = 1000):
        self.error = error
        self.data = data
        self.code = code
    @property
    def dic(self):
        return self.__dict__


class ArticleViewSet(ModelViewSet):


    def list(self, request, *args, **kwargs):
        ret = BaseRespose()
        obj_list = Article.objects.all()
        cs = ArticleSerializers(instance=obj_list,many=True)
        ret.data = cs.data
        return Response(ret.dic)


    # 增加文章评论
    def create(self, request, *args,pk=None, **kwargs):
        ret = BaseRespose()
        try :
            token = request.query_params.get('token')
            content = request.data.get('content')
            article_obj = Article.objects.get(pk=pk)
            user = UserAuthToken.objects.get(token=token).user
            obj = Comment.objects.create(account=user,content=content,content_object=article_obj)
            article_obj.comment_num +=1
            article_obj.save()
            res = CommentSerializers(obj,many=False)
            ret.data = res.data
        except ObjectDoesNotExist as e:
            ret.code = 1001
            ret.error = '查询数据不存在'
        except Exception as e:
            print(e)
            ret.code = 1002
            ret.error = "查询失败"
        return Response(ret.dic)

    def retrieve(self, request, *args,pk=None, **kwargs):
        ret = BaseRespose()
        try:
            obj = Article.objects.get(pk=pk)
            cs = ArticleDetailSerializers(instance=obj,many=False,context={'request': request})
            ret.data = cs.data

        except ObjectDoesNotExist as e:
            ret.code = 1001
            ret.error = '查询数据不存在'
        except Exception as e:
            print(e)
            ret.code = 1002
            ret.error = "查询失败"
        return Response(ret.dic)

