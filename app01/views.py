from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.request import Request
from .models import *
from .service.page import MyPagination
# Create your views here.

from .service.serializerset import *

class BaseResponse:

    def __init__(self,code=1000,error=None,data=None):
        self.code = code
        self.erroe = error
        self.data = data
    def dict(self):
        return self.__dict__

class DegreeCourseView(GenericViewSet):
    # queryset = DegreeCourse.objects.all()
    # serializer_class = DegreeCourseSerializers
    def list(self, request, *args, **kwargs):
        # course_query = DegreeCourse.objects.all()
        # 方式一
        # course_list = list(course_query)
        # import json
        # # ret = json.dumps(course_list,ensure_ascii=False)
        # print('request.user===>',request.user)
        # return JsonResponse(course_list,safe=False,json_dumps_params={'ensure_ascii':False})
        # bs = DegreeCourseSerializers(instance=course_query,many=True)
        # return JsonResponse(bs,json_dumps_params={'ensure_ascii':False},safe=False)

        # 方式二
        course_query = DegreeCourse.objects.all()
        bs = DegreeCourseSerializers(instance=course_query, many=True)
        return JsonResponse(bs.data,safe=False)
        # 方式三
        # ret = BaseResponse()
        # try:
        #     # QuerySet,是django的类型
        #     # 1. 获取数据
        #     course_list = DegreeCourse.objects.all().only('id', 'name').order_by('-id')
        #     # 2. 对数据进行分页
        #     page = MyPagination()
        #     page_course_list = page.paginate_queryset(course_list, request, self)
        #
        #     # 3. 对数据序列化
        #     ser = DegreeCourseSerializers(instance=page_course_list, many=True)
        #     ret.data = ser.data
        # except Exception as e:
        #     ret.code = 1001
        #     ret.error = '获取数据失败'
        # return Response(ret.dict())
    def retrieve(self,request,pk,**kwargs):

        couser_obj = DegreeCourse.objects.filter(pk=pk).first()
        ret = BaseResponse()
        bs = DegreeCourseDetaile(couser_obj,many=False,context={'request':request})
        ret.data = bs.data
        return Response(ret.dict())

class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializers


class PricePolicyViewSet(ModelViewSet):
    queryset = PricePolicy.objects.all()
    serializer_class = PricePolicySerializers

class ContenttypeViewSet(ModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContenttypesSerializers