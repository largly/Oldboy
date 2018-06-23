
from django.utils.deprecation import MiddlewareMixin


class M1(MiddlewareMixin):
    def process_response(self, request, response):
        ret = response
        ret['Access-Control-Allow-Origin']= '*'
        ret['Access-Control-Allow-Headers'] = "Content-Type"
        ret['Access-Control-Allow-Methods']= "PUT,DELETE"
        ret['Access-Control-Max-Age']= 10
        return ret