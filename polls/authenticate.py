
from rest_framework.authentication import TokenAuthentication
from polls.models import StaticToken

class StaticTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'
    model = StaticToken
