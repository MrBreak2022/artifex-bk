from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["id","_id", "email", "username", "password", "isAdmin"]

    def get__id(self, obj):
        return obj.id
    def get_isAdmin(self, obj):
        return obj.is_staff

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'],
                                       username=validated_data['username'],
                                       paypalemail=validated_data['paypalemail']
                                         )
        user.set_password(validated_data['password'])
        user.save()
        return user  
     
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id','_id','username', 'email', 'isAdmin', 'token', 'password', 'paypalemail']  

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    
    def get__id(self, obj):
        return obj.id
    
    def get_paypalemail(self, obj):
        return obj.paypalemail

    