from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_out
from knox.auth import TokenAuthentication
from knox.views import LoginView, LogoutView, LogoutAllView
from knox.models import AuthToken
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError

class LoginView(LoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        try:
            user = User.objects.get(username=request.data['username'])
            AuthToken.objects.filter(user=user.id).all().delete()
            serializer = AuthTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']  
            login(request, user)
            response = super(LoginView, self).post(request, format=None)
            return response
        except Exception as e:
            try:
                if e.detail['non_field_errors'][0]:
                    return Response('wrong password or username')
            except:
                return Response('user not found')


class LogoutView(LogoutView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        request._auth.delete()
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)  
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    

class LogoutAllView(LogoutAllView):
    '''
    Log the user out of all sessions
    I.E. deletes all auth tokens for the user
    '''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        request.user.auth_token_set.all().delete()
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        print('logoutAll')
        return Response(None, status=status.HTTP_204_NO_CONTENT)