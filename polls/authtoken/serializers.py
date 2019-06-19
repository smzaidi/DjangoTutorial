from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:

            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')    
        # The authenticate call simply returns None for is_active=False
        # users. (Assuming the default ModelBackend authentication
        # backend.)
            # if not user:
            #     user = User.objects.get_by_natural_key(username)
            #     print(user)
            #     print(password)
            #     print('---------------------------/')
            #     if not user:
            #         msg = _('Unable to log in with provided credentials.')
            #         raise serializers.ValidationError(msg, code='authorization')
            #     else:
            #         pass
            # else:
            #     pass
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        print(user)
        print('-----------')
        return attrs
