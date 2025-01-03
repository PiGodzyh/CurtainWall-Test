from django.http import HttpResponseForbidden
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication


class IsSuperUser(BasePermission):
    # 无权限时返回给前端的信息
    message = {
        "code": 403,
        "message": "无系统管理员权限"
    }

    def has_permission(self, request, view):
        """控制对obj对象的访问权限，此案例决绝所有对对象的访问"""
        return request.user.is_superuser


class IsSystemAUser(BasePermission):
    # 无权限时返回给前端的信息
    message = {
        "code": 403,
        "message": "无系统A权限"
    }
    """
            检查用户是否具有系统A的访问权限。

            参数:
            - request (HttpRequest): 请求对象。
            - view (APIView): 视图对象。

            返回值:
            - bool: 如果用户具有系统A的权限则返回 True，否则返回 False。
    """

    def has_permission(self, request, view):
        """控制对obj对象的访问权限，此案例决绝所有对对象的访问"""
        # token = request.META.get('Authorization')
        # # payload=JWTAuthentication.get_user(token)
        return request.user.access_system_a


class IsSystemBUser(BasePermission):
    # 无权限时返回给前端的信息
    message = {
        "code": 403,
        "message": "无系统B权限"
    }

    def has_permission(self, request, view):
        """控制对obj对象的访问权限，此案例决绝所有对对象的访问"""
        return request.user.access_system_b


class IsSystemCUser(BasePermission):
    # 无权限时返回给前端的信息
    message = {
        "code": 403,
        "message": "无系统C权限"
    }

    def has_permission(self, request, view):
        """控制对obj对象的访问权限，此案例决绝所有对对象的访问"""
        return request.user.access_system_c


class IsSystemDUser(BasePermission):
    # 无权限时返回给前端的信息
    message = {
        "code": 403,
        "message": "无系统D权限"
    }

    def has_permission(self, request, view):
        """控制对obj对象的访问权限，此案例决绝所有对对象的访问"""
        return request.user.access_system_d


class IsSystemVUser(BasePermission):
    # 无权限时返回给前端的信息
    message = {
        "code": 403,
        "message": "无系统E权限"
    }

    def has_permission(self, request, view):
        """控制对obj对象的访问权限，此案例决绝所有对对象的访问"""
        return request.user.access_system_v


class IsSystemFUser(BasePermission):
    # 无权限时返回给前端的信息
    message = {
        "code": 403,
        "message": "无系统F权限"
    }

    def has_permission(self, request, view):
        """控制对obj对象的访问权限，此案例决绝所有对对象的访问"""
        return request.user.access_system_f


class IsSystemGUser(BasePermission):
    # 无权限时返回给前端的信息
    message = {
        "code": 403,
        "message": "无系统G权限"
    }

    def has_permission(self, request, view):
        """控制对obj对象的访问权限，此案例决绝所有对对象的访问"""
        return request.user.access_system_g


class IsSystemHUser(BasePermission):
    # 无权限时返回给前端的信息
    message = {
        "code": 403,
        "message": "无系统H权限"
    }

    def has_permission(self, request, view):
        """控制对obj对象的访问权限，此案例决绝所有对对象的访问"""
        return request.user.access_system_h
    
class IsSystemZUser(BasePermission):
    # 无权限时返回给前端的信息
    message = {
        "code": 403,
        "message": "无系统H权限"
    }

    def has_permission(self, request, view):
        """控制对obj对象的访问权限，此案例决绝所有对对象的访问"""
        return request.user.access_system_z
