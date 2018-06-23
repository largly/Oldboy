from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from datasource.models import Account,UserAuthToken

class Login(APIView):

    def post(self,request):

        username = request.data.get('username')
        pwd = request.data.get('pwd')
        res = {'code':1000,'error':None,'token':None,username:None}
        ret = Account.objects.filter(username=username,password=pwd).first()
        if ret:
            obj = UserAuthToken.objects.update_or_create(user=ret)[0]
            res['token'] = obj.token
            res['username']=username
        else:
            res['error'] = '用户名密码错误'
        return JsonResponse(res)