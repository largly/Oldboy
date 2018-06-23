from rest_framework.authentication import BasicAuthentication
from datasource.models import Account,UserAuthToken

class MyAuthentication(BasicAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token')
        user = Account.objects.filter(userauthtoken__token=token)
        if user:
            return user.first(),None