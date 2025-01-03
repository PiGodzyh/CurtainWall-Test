#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
"""
Django 的命令行工具，用于执行各种管理任务。

此脚本提供了运行 Django 项目所需的各种管理命令，包括但不限于：
- 启动开发服务器
- 迁移数据库
- 创建超级用户
- 测试项目等

使用方法：
- 启动开发服务器：`python manage.py runserver`
- 创建超级用户：`python manage.py createsuperuser`
- 迁移数据库：`python manage.py migrate`
- 更多命令：`python manage.py help`

注意：
- 确保激活了正确的虚拟环境。
- 确认 Django 已正确安装。

"""

def main():

    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AccountManagement.settings")
    try:
        from django.core.management import execute_from_command_line

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    print("Document:http://127.0.0.1:8000/doc")
    print("Document:http://127.0.0.1:8000/redoc")
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
