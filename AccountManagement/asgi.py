import os

from django.core.asgi import get_asgi_application

"""
ASGI 配置文件用于 AccountManagement 项目。

此文件暴露了一个名为 `application` 的 ASGI 可调用对象。

更多信息，请参见：
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/

"""

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AccountManagement.settings")

application = get_asgi_application()
