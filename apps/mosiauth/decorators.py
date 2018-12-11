from utils import restful
from django.shortcuts import redirect



# 装饰器,如果用户没有登陆,返回一些消息
def blog_login_required(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        else:
            if request.is_ajax():
                return restful.unauth(message='请先登录！')
            else:
                return redirect('/')

    return wrapper