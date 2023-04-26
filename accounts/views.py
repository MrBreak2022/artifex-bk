from django.shortcuts import get_object_or_404, render
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import *
from base.serializers import *
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        # data["username"] = self.user.username
        data["email"] = self.user.email
        for k, v in serializer.items():
            data[k] = v
        return data    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializerWithToken(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializerWithToken(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request,pk):
    users = User.objects.get(id=pk)
    serializer = UserSerializer(users,many = False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    data = request.data

    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    
    if data.get('password'):
        user.set_password(data['password'])

    user.save()

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def updateUser(request, pk):
    user = get_object_or_404(User, id=int(pk))

    data = request.data
    user.username = data['username']
    user.email = data['email']
    # user.password = user.password
    # if data['password'] != '':
    #     user.password = data['password']
    user.save()

    return Response(UserSerializer(user).data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    return Response('User Deleted')

