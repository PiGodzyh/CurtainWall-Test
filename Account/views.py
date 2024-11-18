import json

from django.forms import model_to_dict
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import *
from rest_framework.viewsets import GenericViewSet

from AccountManagement.permission import *
from Account.models import *
from Account.serializers import UserSerializer, process_user
# from rest_framework.authtoken.models import Token

from Account.util import sendemail
from Account.util import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from AccountManagement.swagger import CustomSwaggerAutoSchema

# 存储邮箱和验证码的字典
validate_data = {}

# 账号类
# 功能：用于账号相关操作
# 包括方法：
#   sendCode：给邮箱发验证码
#   validate：验证验证码
#   getSubsysUser：获取某个子系统下的所有账户 
class Account(GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = []
    permission_classes = []

    swagger_tags = ["Account"]

    sendCode_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='邮箱'),
        }
    )
    # API：给邮箱发验证码
    # 参数：
    #   email：用户邮箱
    # 返回值：
    #   若邮箱已被注册：400 和相应信息
    #   若发送成功：200 和相应信息
    @csrf_exempt
    @swagger_auto_schema(
        method='POST',
        request_body=sendCode_body,
        operation_description="POST /account/sendCode/")
    @action(methods=['POST'], detail=False)
    def sendCode(self, request):
        # postman测试用raw
        data = json.loads(request.body)
        email = data.get('email')

        # 检查邮箱是否已被注册
        if User.objects.filter(email=email).exists():
            return JsonResponse({'message': '该邮箱已经注册'}, status=400)

        # 生成验证码并发送
        code = get_random_string(length=4, allowed_chars='0123456789')
        sendemail(code, email)  # 出错点
        validate_data[email] = code
        return Response.OkResponseMessage('验证码已发送，请检查您的邮箱')


    validate_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password','code'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING,  description='邮箱'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码'),
            'code': openapi.Schema(type=openapi.TYPE_STRING, description='验证码'),
        }
    )
    # API：验证验证码
    # 参数：
    #   email：用户邮箱
    #   password：用户密码
    #   code：验证码
    # 返回值：
    #   若验证码错误或已过期：400 和相应信息
    #   若注册成功：200 和相应信息
    @csrf_exempt
    @swagger_auto_schema(
        method='POST',
        request_body=validate_body,
        operation_description="POST /account/validate/")
    @action(methods=['POST'], detail=False)
    def validate(self, request):
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        code = data.get('code')
        # 检查验证码
        if email in validate_data and validate_data[email] == code:
            # 创建新用户
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()
            return Response.OkResponseMessage('注册成功')

        return Response.ErrorResponse(400,'验证码错误或已过期')

    getSubsysUser_sysname = openapi.Parameter('sysname', openapi.IN_QUERY, description="system name", type=openapi.TYPE_STRING)
    # API：获取某个子系统下的所有账户
    # 参数：
    #   sysname：子系统名称
    # 返回值：
    #   userDict：账户邮箱列表
    @csrf_exempt
    @swagger_auto_schema(
        method='GET',
        manual_parameters=[getSubsysUser_sysname],
        operation_description="GET /account/getSubsysUser/")
    @action(methods=['GET'], detail=False)
    def getSubsysUser(self, request):
        sysIndex=request.GET.get('sysname')
        # print(sysIndex)
        # return QuerySet object
        userQuerySet=User.objects.filter(**{"access_system_"+sysIndex: True}).values("email")
        userDict = {"email": []}
        for entry in userQuerySet:
            userDict["email"].append(entry['email'])
        # userDict=[entry for entry in userQuerySet]  # converts ValuesQuerySet into Python list
        # print(userDict)

        return Response.OkResponseData(userDict)

# 超级权限类
# 功能：用于超级用户进行权限相关操作
# 包括方法：
#   updatePermission：更新用户权限
#   getAllPermissions：获取所有用户的权限信息
class SuperPermission(GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperUser]

    swagger_tags = ["SuperPermission"]

    updatePermission_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username1': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'system_access_a': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'system_access_b': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                }
            ),
            'username2': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'system_access_c': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'system_access_d': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'system_access_e': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                }
            )
        }
    )
    # API：更新用户权限
    # 参数：
    #     user: 包含用户权限信息的对象，包括username和permission属性。
    # 返回值：
    #     若更新成功：200 和相应信息
    #     若更新失败：400 和相应信息
    @csrf_exempt
    @swagger_auto_schema(
        method='POST',
        request_body=updatePermission_body,
        operation_description="POST /account/updatePermission/")
    @action(methods=['POST'], detail=False)
    def updatePermission(self, request):
        users = json.loads(request.body)
        result = process_user(users)
        if result:
            return Response.OkResponse()
        else:
            return Response.ErrorResponse(400,"邮箱不存在或权限未更改")
    # API：获取所有用户的权限信息
    # 返回值：
    #     所有用户的权限信息
    @csrf_exempt
    @swagger_auto_schema(
        method='GET',
        manual_parameters=[],
        operation_description="GET /account/getAllPermissions/")
    @action(methods=['GET'], detail=False)
    def getAllPermissions(self, request):
        users = User.objects.all()
        users_dict = {}
        for user in users:
            users_dict[user.username] = {}
            user_dict = users_dict[user.username]
            temp = model_to_dict(user)
            user_dict['is_superuser'] = temp['is_superuser']
            user_dict['access_system_a'] = temp['access_system_a']
            user_dict['access_system_b'] = temp['access_system_b']
            user_dict['access_system_c'] = temp['access_system_c']
            user_dict['access_system_d'] = temp['access_system_d']
            user_dict['access_system_e'] = temp['access_system_e']
            user_dict['access_system_f'] = temp['access_system_f']
            user_dict['access_system_g'] = temp['access_system_g']
            user_dict['access_system_h'] = temp['access_system_h']

        return Response.OkResponseData(users_dict)


# 用户权限类
# 功能：用于获取当前用户的权限信息
class CustomPermission(GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    swagger_tags = ["CustomPermission"]
    # API：获取当前用户的权限信息
    # 参数：
    #   user：用户
    # 返回值：
    #   当前用户的权限信息
    @csrf_exempt
    @swagger_auto_schema(
        method='GET',
        manual_parameters=[],
        operation_description="GET /account/getPermissions/")
    @action(methods=['GET'], detail=False)
    def getPermissions(self, request):
        print(request.user)
        user=User.objects.get_by_natural_key(request.user)
        temp = model_to_dict(user)
        permission_dict = {}
        permission_dict['is_superuser'] = temp['is_superuser']
        permission_dict['access_system_a'] = temp['access_system_a']
        permission_dict['access_system_b'] = temp['access_system_b']
        permission_dict['access_system_c'] = temp['access_system_c']
        permission_dict['access_system_d'] = temp['access_system_d']
        permission_dict['access_system_e'] = temp['access_system_e']
        permission_dict['access_system_f'] = temp['access_system_f']
        permission_dict['access_system_g'] = temp['access_system_g']
        permission_dict['access_system_h'] = temp['access_system_h']
        return Response.OkResponseData(permission_dict)



