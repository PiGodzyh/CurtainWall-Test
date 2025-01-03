from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from Account.models import User
from Account.util import Response

# 类名：UserSerializer
# 功能：提供User类的序列化功能
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# class ResponseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Response
#         fields = '__all__'

# 类名：MyTokenObtainPairSerializer
# 功能：令牌相关功能，继承自TokenObtainPairSerializer，重写部分方法
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # 功能：按照User类，重写获取JWT令牌方法
    # 参数：
    #   user：object，包含用户的全部数据
    # 返回值：
    #   token：object，用户令牌
    @classmethod
    def get_token(cls, user):
        # 通过父类方法获取token
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['access_system_a']=user.access_system_a
        token['access_system_b'] = user.access_system_a
        token['access_system_c'] = user.access_system_b
        token['access_system_d'] = user.access_system_c
        token['access_system_v'] = user.access_system_v
        token['access_system_f'] = user.access_system_f
        token['access_system_g'] = user.access_system_g
        token['access_system_h'] = user.access_system_h
        token['access_system_z'] = user.access_system_z

        return token

    # 功能：重写验证用户信息的方法
    # 参数：
    #   attrs：包含需要验证的用户信息
    # 返回值：
    #   response_data：object，包含验证成功或失败的信息，若成功则额外包含令牌信息
    def validate(self, attrs):
        # print(attrs)
        # print(self)
        user = authenticate(username=attrs.get('username'), password=attrs.get('password'))
        authentication=False
        response_data={}
        if user is not  None:
            authentication=True
            data = super().validate(attrs)
            response_data['token'] = data["access"]
        else:
            authentication= False

        response_data["authentication"]=authentication

        # 添加额外的返回信息
        # data['username'] = self.user.username
        return response_data


# 视图类关联新定义的序列化器
# 用于处理获取JWT令牌的请求
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# 功能：用户权限更新
# 参数：
#   users：object，包含多个users数据
#       username：string
#       permission：object，包含一个用户的所有权限
def process_user(users):
    print("输入内容为：",users)
    old_user = ""
    for username, permissions in users.items():
        if username == "admin":
            return True
        if permissions.get('method') == "table":
            old_user = User.objects.get_by_natural_key(username)
            pass
        else:
            try:
                old_user = User.objects.get_by_natural_key(username)
            except:
                return False
        for permission, value in permissions.items():
            old_value = getattr(old_user, permission)
            # 检查权限是否被修改
            if old_value != value:
                setattr(old_user, permission, value)
                old_user.save()
                return True
            else:
                print("权限未变，无需修改")
                return False