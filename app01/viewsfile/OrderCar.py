from django.http import HttpResponse, JsonResponse
from django_redis import get_redis_connection
import json
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from app01.service.baseresponse import BaseRespose
from datasource.models import *
from datasource import models
from app01.service.auth import MyAuthentication
class OrderCar(GenericAPIView):
    authentication_classes = [MyAuthentication,]
    def get(self,request,*args,**kwargs):

        user_id = request.user.id
        conn = get_redis_connection()
        # conn.hset('n1', 'k1', 'v1')
        ret = BaseRespose()
        data_temp = conn.hget('luffy_shopping_car',user_id)
        # data = {k.decode():json.loads(v.decode()) for k,v in data_temp.items()}
        data_temp  = json.loads(data_temp.decode())
        ret.dat = data_temp
        return JsonResponse(ret.dic,json_dumps_params={'ensure_ascii':False})

    def post(self, request, *args, **kwargs):
        conn = get_redis_connection()
        ret = BaseRespose()
        token = request.query_params.get('token')
        user_id = UserAuthToken.objects.get(token=token).user_id
        course_id = request.data.get('id')

        course_type = request.data.get('course_type')
        course_class= getattr(models,course_type.capitalize())
        course_obj = course_class.objects.get(pk = course_id)
        price_policy_dict = {str(obj.valid_period):{'period_name':obj.get_valid_period_display(),'price':obj.price} for obj in course_obj.price_policy.all()}
        temp_dict = {course_id:{
            'course_type':course_type,
            'id':course_id,
            'name':course_obj.name,
            'img':course_obj.course_img,
            'selected_policy': 1
        }}
        temp_dict['price_policy_dict']=price_policy_dict

        conn.hset('luffy_shopping_car',user_id,json.dumps(temp_dict))
        data = conn.hget('luffy_shopping_car',user_id)
        ret.data = json.loads(data.decode())

        return Response(ret.dic)
        data = '''luffy_shopping_car: {
							用户ID: {
								课程A ID: {
									id: 1,
									name: '金融量化分析入门',
									img:'../xxxx.png'
									selected_policy:1,
									price_policy_dict:{
										1: {period:30,price:599},
										2: {period:60,price:1599},
										3: {period:90,price:2599},
									}
									
								}
					                    }
        '''


    def patch(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        policy_id = request.data.get('policy_id')
        user_id = request.user.id
        conn = get_redis_connection()
        # conn.hset('n1', 'k1', 'v1')
        ret = BaseRespose()
        data_temp = conn.hget('luffy_shopping_car', user_id)
        # data = {k.decode():json.loads(v.decode()) for k,v in data_temp.items()}
        course_dict = json.loads(data_temp.decode())
        course_dict[str(course_id)]['selected_policy'] = policy_id
        conn.hset('luffy_shopping_car',user_id,course_dict)
        ret.dat = data_temp
        return JsonResponse(ret.dic, json_dumps_params={'ensure_ascii': False})

        # return HttpResponse('....')

    def delete(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        token = request.query_params.get('token')
        conn = get_redis_connection()
        # conn.hset('n1', 'k1', 'v1')
        user_id = UserAuthToken.objects.get(token=token).user_id
        ret = BaseRespose()
        data_temp = conn.hgetall('luffy_shopping_car',user_id)
        # data = {k.decode():json.loads(v.decode()) for k,v in data_temp.items()}
            # print(json.loads(v))
        course_dict = json.loads(data_temp.decode())
        course_dict.pop(str(course_id),None)
        data = conn.hget('luffy_shopping_car', user_id)
        return JsonResponse(ret.dic, json_dumps_params={'ensure_ascii': False})


class Blance(GenericAPIView):

    def get(self,request):
        today = datetime.date.today()
        conn = get_redis_connection('default')
        user_id = request.user.id
        prolicy_dict_str = conn.hget('luffy_prolicy_dict', user_id)
        prolicy_dict = json.loads(prolicy_dict_str.decode())
        for k in prolicy_dict:
            for i in  prolicy_dict[k]['conpon']:
                if prolicy_dict[k]['conpon'][i]['valid_end_date']<today:
                    del prolicy_dict[k]['conpon'][i]
        return JsonResponse(prolicy_dict)

    def post(self,request):
        user_id = request.user.id
        conn = get_redis_connection('default')
        today = datetime.date.today()
        coupon_list = Coupon.objects.filter(couponrecord__account=request.user,
                                            couponrecord__status_choices=1,
                                            valid_begin_date__lt=today,
                                            valid_end_date__gt=today
                                            )
        course_list = request.data.get('course')
        course_dict_str = conn.hget('luffy_shopping_car', user_id)
        course_dict = json.loads(course_dict_str.decode())
        temp = {}
        for k,v in course_dict:
            if k in course_list:
                v['price_policy']=v['price_policy_dict']['selected_policy']
                del v['price_policy_dict']
                temp[k] = v
        for obj in coupon_list:
            if obj.object_id in course_list:
                if not temp[obj.object_id].haskey('selected_conpon'):
                    temp[obj.object_id]['conpon'] = {}
                    temp[obj.object_id]['selected_conpon'] = obj.object_id
                temp[obj.object_id]['conpon'][obj.object_id]={'conpon_id':obj.object_id,'name':obj.name,'valid_end_date':obj.valid_end_date}
        prolicy_dict = temp
        conn.hset('luffy_prolicy_dict', user_id,json.dumps(prolicy_dict))
    def dispatch(self, request, *args, **kwargs):
        pass
    def delete(self,request):
        pass