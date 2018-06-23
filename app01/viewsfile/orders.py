from uuid import uuid4

from django.http import HttpResponse, JsonResponse
from django_redis import get_redis_connection
import json

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from app01.service.baseresponse import BaseRespose
from datasource.models import *
from datasource import models


class Order(GenericAPIView):

    def post(self,request):
        ret = BaseRespose()
        user = request.useer
        order_number = uuid4()
        payment_type = request.form.get('pay_type')
        actual_amount = request.form.get('actual_amount')
        # real_amount =

    def get(self):
        pass
    def delete(self):
        pass
    def patch(self):
        pass
