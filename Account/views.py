import json
import re

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
        required=['email','method'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='邮箱'),
            'method': openapi.Schema(type=openapi.TYPE_STRING, description='邮箱', enum=['register','reset']),
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
        data = json.loads(request.body)
        email = data.get('email')
        method = data.get('method')
        if method not in ['register', 'reset']:
            return JsonResponse({'message': '无效的请求'}, status=400)

        if method == 'register':
            # 检查邮箱是否已被注册
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': '该邮箱已经注册'}, status=400)
            # 验证邮箱格式
            if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                return JsonResponse({'message': '邮箱格式不正确'}, status=400)
            
        if method == 'reset':
            # 检查邮箱是否存在
            if not User.objects.filter(email=email).exists():
                return JsonResponse({'message': '用户不存在'}, status=400)

        # 生成验证码并发送
        code = get_random_string(length=4, allowed_chars='0123456789')

        sendemail("幕墙验证码", '您的幕墙验证码是：' + code, email)  # 出错点
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
    # API：验证验证码并
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
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            # 检查密码是否为空
            if not password:
                return Response.ErrorResponse(400, '密码不能为空')
            code = data.get('code')

            # 检查验证码
            if email in validate_data and validate_data[email] == code:
                try:
                    # 尝试获取用户
                    user = User.objects.get(email=email)
                    # 如果用户已存在，修改密码
                    user.set_password(password)
                    user.save()
                    del validate_data[email]  # 删除验证码，防止重复使用
                    return Response.OkResponseMessage('密码修改成功')
                except User.DoesNotExist:
                    # 如果用户不存在，创建新用户
                    user = User.objects.create_user(username=email, email=email, password=password)
                    user.save()
                    # 向管理员发送注册成功邮件
                    admin=User.objects.get(is_superuser=True)
                    sendemail("注册成功", '新用户注册：' + email, admin.email)
                    del validate_data[email]  # 删除验证码，防止重复使用
                    return Response.OkResponseMessage('注册成功')
            else:
                return Response.ErrorResponse(400, '验证码错误或已过期')
        except Exception as e:
            return Response.ErrorResponse(500, f'服务器错误: {str(e)}')

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
        
    # API：获取指定用户的权限信息
    # 参数：
    #     username：用户名搜索关键字
    # 返回值：
    #     所有用户的权限信息
    @csrf_exempt
    @swagger_auto_schema(
        method='GET',
        manual_parameters=[
            {
                "name": "username",
                "in": "query",
                "description": "搜索包含指定关键字的用户名",
                "required": False,
                "type": "string"
            }
        ],
        operation_description="GET /account/getUserPermissions/")
    @action(methods=['GET'], detail=False, permission_classes=[AllowAny])
    def getUserPermissions(self, request):
        username = request.GET.get('username', None)  # 获取查询参数 username
        users = User.objects.all()

        if username:
            # 如果提供了 username 参数，则过滤用户
            users = users.filter(username__icontains=username)

        users_dict = {}
        for user in users:
            users_dict[user.username] = {
                'is_superuser': user.is_superuser,
                'access_system_a': user.access_system_a,
                'access_system_b': user.access_system_b,
                'access_system_c': user.access_system_c,
                'access_system_d': user.access_system_d,
                'access_system_v': user.access_system_v,
                'access_system_f': user.access_system_f,
                'access_system_g': user.access_system_g,
                'access_system_h': user.access_system_h,
                'access_system_z': user.access_system_z,
            }

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
        permission_dict['access_system_v'] = temp['access_system_v']
        permission_dict['access_system_f'] = temp['access_system_f']
        permission_dict['access_system_g'] = temp['access_system_g']
        permission_dict['access_system_h'] = temp['access_system_h']
        permission_dict['access_system_z'] = temp['access_system_z']
        return Response.OkResponseData(permission_dict)



