from rest_framework import serializers
from .models import UserModel
from djoser.serializers import UserCreateSerializer


class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ["id",'email', 'username','first_name',"last_name","date_joined","mobile_no","is_mobile_verified","profile_picture"]




class UserCreateSerializer(UserCreateSerializer):
    # password = serializers.CharField(write_only=True)
    class Meta(UserCreateSerializer.Meta):
        model = UserModel
        fields = "__all__"
        # fields = ["id",'email', 'username','first_name',"last_name","date_joined","mobile_no","is_mobile_verified","profile_picture"]

