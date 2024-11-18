from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from Account.views import SuperPermission, CustomPermission
from Account.serializers import MyTokenObtainPairView
from Account.views import Account

# 路由配置
# 调用API从此处调，as_view中的参数限制了该API允许使用的方法，无参数则无限制。
# 调用方法（以sendcode为例）：
#   POST host:port/sendCode
#   此时就会调用Accont中的sendCode方法 
urlpatterns = [
 path('login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
 # path('token/refresh', MyTokenObtainPairView.as_view(), name='token_refresh'),
 # # 下面这个是用来验证token的，根据需要进行配置
 # path('token/verify', MyTokenObtainPairView.as_view(), name='token_verify'),

 # path('login', Account.as_view({'post':'login'})),
 path('sendCode', Account.as_view({'post':'sendCode'})),
 path('validate', Account.as_view({'post':'validate'})),
 path('getSubsysUser',Account.as_view({'get':'getSubsysUser'})),

 path('super/updatePermission', SuperPermission.as_view({'post':'updatePermission'})),
 path('super/getAllPermissions', SuperPermission.as_view({'get':'getAllPermissions'})),

 path('custom/getPermissions',CustomPermission.as_view({'get':'getPermissions'})),


]
