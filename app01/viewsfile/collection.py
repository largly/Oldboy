from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from datasource.models import *
from app01.service.serializerset import *
from rest_framework.parsers import JSONParser

from ..service.baseresponse import BaseRespose

class CollectionViewSet(ModelViewSet):


    def list(self, request, *args, **kwargs):
        ret = BaseRespose()
        obj_list = Collection.objects.all()
        cs = CollectionSerializers(instance=obj_list,many=True)
        ret.data = cs.data
        return Response(ret.dic)

    def create(self, request, *args,pk=None, **kwargs):
        ret = BaseRespose()
        try :
            token = request.query_params.get('token')
            user = UserAuthToken.objects.get(token=token).user
            table_name = request.data.get('table')
            id = request.data.get('id')
            if table_name == 'article':
                content_object = Article.objects.get(id=id)
                content_object.collect_num += 1
                content_object.save()
            else:
                content_object = CourseSection.objects.get(id=id)
            obj = Collection.objects.create(account=user,content_object=content_object)
            res = CollectionSerializers(obj,many=False)
            ret.data = res.data
        except ObjectDoesNotExist as e:
            ret.code = 1001
            ret.error = '查询数据不存在'
        except Exception as e:
            print(e)
            ret.code = 1002
            ret.error = "查询失败"
        return Response(ret.dic)


