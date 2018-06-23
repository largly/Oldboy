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


class CourseViewSet(ModelViewSet):


    def list(self, request, *args, **kwargs):
        ret = BaseRespose()
        obj_list = Course.objects.all().only('id','name')
        cs = CourseSerializers(instance=obj_list,many=True)
        ret.data = cs.data
        return Response(ret.dic)

    def retrieve(self, request, *args,pk=None, **kwargs):
        ret = BaseRespose()
        try:
            obj =  Course.objects.get(pk=pk)
            cs = CourseDetaileSerializers(instance=obj,many=False,context={'request': request})
            ret.data = cs.data

        except ObjectDoesNotExist as e:
            ret.code = 1001
            ret.error = '查询数据不存在'
        except Exception as e:
            print(e)
            ret.code = 1002
            ret.error = "查询失败"
        return Response(ret.dic)

