import base64
import json
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.http import JsonResponse, HttpResponse

# 功能：发送邮箱验证码
# 参数：
#   code：验证码
#   destination：目标邮箱    
def sendemail(code, destination):
    # 检查验证码或邮箱地址是否为空
    if not code or not destination:
        raise ValueError('验证码或邮箱地址为空')

    # 检查验证码是否为四位数字
    if not code.isdigit() or len(code) != 4:
        raise ValueError('验证码必须是四位数字')

    # 检查邮箱地址是否合法
    if '@' not in destination or '.' not in destination:
        raise ValueError('邮箱地址不合法')

    # 1. 连接邮箱服务器
    con = smtplib.SMTP_SSL('smtp.qq.com', 465)

    sender_account = "237793303@qq.com"  # ！！！请不要一直使用同一个邮箱
    sender_account_passcode = "hvmzeatnquaacagj" # 授权码

    # 2. 登录邮箱
    con.login(sender_account, sender_account_passcode)


    # 2. 准备数据
    # 创建邮件对象
    msg = MIMEMultipart()
    # 设置邮件主题
    subject = Header('幕墙系统注册验证码', 'utf-8').encode()
    msg['Subject'] = subject
    # 设置邮件发送者
    # msg['From'] = 'TongjiSE@tongji.edu.cn'
    fromName64 = base64.b64encode(bytes("神猪降世", 'utf-8'))
    fromName64str = str(fromName64, 'utf-8')
    # 尖括号拼接用双引号
    fromNamestr = '"=?utf-8?B?' + fromName64str + '=?=" <' + sender_account + ">"
    msg['From']=Header(fromNamestr)
    # 设置邮件接受者
    msg['To'] = Header(destination)
    # 验证码内容
    text = MIMEText('注册验证码是：'+code, 'plain', 'utf-8')
    msg.attach(text)
    # 3.发送邮件
    con.sendmail(sender_account, destination, msg.as_string())
    con.quit()

# 定义response静态类，供接口返回值使用
class Response():
    code=200
    message="成功"
    data=""

    def keys(self):
        '''当对实例化对象使用dict(obj)的时候, 会调用这个方法,这里定义了字典的键, 其对应的值将以obj['name']的形式取,
       但是对象是不可以以这种方式取值的, 为了支持这种取值, 可以为类增加一个方法'''
        return ('code', 'message', 'data')

    def __getitem__(self, item):
        '''内置方法, 当使用obj['name']的形式的时候, 将调用这个方法, 这里返回的结果就是值'''
        return getattr(self, item)


    @staticmethod
    def OkResponse():
        return JsonResponse({'code':200,'message':"成功"})

    @staticmethod
    def OkResponseData(data):
        print(data)
        return JsonResponse({'code':200,'message':"成功",'data':data})

    @staticmethod
    def OkResponseMessage(message):
        return JsonResponse({'code': 200, 'message': message })

    @staticmethod
    def ErrorResponse(code, message):
        return JsonResponse({'code': code, 'message': message}, status=code)