from django.shortcuts import render
from .models import ArticleCategory,Article,Comment
from django.conf import settings
from .serializers import ArticleSerializer,CommentSerizlizer
from utils import restful
from .forms import PublicCommentForm
from apps.mosiauth.decorators import blog_login_required


# 主页视图函数
def index(request):

    count = settings.ONE_PAGE_NEWS_COUNT

    # select_related提前查找外键，提高sql查询性能（外键都能以这种形式来运行）
    acrticles = Article.objects.select_related('category','author').all()[0:count]
    categories = ArticleCategory.objects.all()
    # 随机抽取12条给推荐内容
    results = Article.objects.order_by('?')[:12]
    article_recommend = list(results)
    context = {
        'categories': categories,
        'acrticles' :acrticles,
        'article_recommend':article_recommend
    }
    return render(request,'article/index.html',context=context)


# 文章详细页视图函数
def article_detail(request,article_id):
    # 获取pk, 内容等于传进来的id
    # select_related提前查找外键，提高sql查询性能（外键都能以这种形式来运行）
    articles = Article.objects.select_related('category','author').get(pk=article_id)

    # 随机抽取6条给热门内容
    results = Article.objects.order_by('?')[:6]
    article_recommend = list(results)
    context = {
        'articles': articles,
        'article_recommend':article_recommend
    }

    return render(request,'article/article_detail.html',context=context)


# 登陆页面视图函数
def logon_view(request):
    return render(request,'article/login.html')

# 注册页面视图函数
def lognup_view(request):
    return render(request,'article/register.html')


# 文章列表（点击加载更多部分）
def article_list(request):
    # 1.获取页数p, 默认方式页数为1，
    page = int(request.GET.get('p',1))

    # 获取分类的Id,默认id=0,等于0就等于不分类
    category_id = int(request.GET.get('category_id',0))


    # 假设ONE_PAGE_NEWS_COUNT = 5
    # 如果传进来的是1，其实值则是0，结束值是5那么就是0：5之间的数据
    # page = 1 的时候 start0：end5
    # page = 2 的时候，start5:end10
    # page = 3的时候 ，start10:end15
    # page由前端传入，每点击一次的时候page加1

    # 起始页数
    start = (page-1)*settings.ONE_PAGE_NEWS_COUNT
    # 结束页数
    end = start + settings.ONE_PAGE_NEWS_COUNT

    # 如果分类等于0
    if category_id == 0:
        # 取值
        # select_related提前查找外键，提高sql查询性能（外键都能以这种形式来运行）
        article = Article.objects.select_related('category','author').all()[start:end]

    else:

        # 实验是否需要两个下划线
        # 提取出所有相关id的内容
        # select_related提前查找外键，提高sql查询性能（外键都能以这种形式来运行）
        article = Article.objects.select_related('category','author').filter(category__id=category_id)[start:end]
    # 进行序列化操作
    serializers = ArticleSerializer(article,many=True)
    # 取出data值
    data = serializers.data

    return restful.result(data=data)

# 发表评论
@blog_login_required
def public_comment(request):
    form  = PublicCommentForm(request.POST)
    if form.is_valid():
        article_id = form.cleaned_data.get('article_id')
        content = form.cleaned_data.get('content')
        article = Article.objects.get(pk=article_id)
        comment = Comment.objects.create(content=content,article=article,author=request.user)
        serizlize = CommentSerizlizer(comment)
        return restful.result(data=serizlize.data)
    else:
        return restful.params_error(message=form.get_errors())


