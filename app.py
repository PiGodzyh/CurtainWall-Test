from django.http import JsonResponse
from django.urls import path
from django.conf import settings

def test(request):
    return JsonResponse({"message": "智慧幕墙——用户鉴权系统"})

settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=['*']
)

urlpatterns = [
    path('test', test),
]

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(['', 'runserver', '0.0.0.0:8080'])