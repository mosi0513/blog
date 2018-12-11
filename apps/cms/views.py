from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_POST
from utils import restful
from apps.article.models import ArticleCategory,Article
from .forms import EditArticleCategoryForm,WriteArticleForm,EditArticleForm
import os
from django.conf import settings
from django.views.generic import View
from django.core.paginator import Paginator
from datetime import datetime
from django.utils.timezone import make_aware
from urllib import parse
from django.db.models import Count
# cms首页
@staff_member_required(login_url='/')
def cms_index(request):
    return render(request,'cms/cms_index.html')



# 文章分类的模板
def article_category(request):
    # 一般的这个在柱模板进行映射
    # categories = ArticleCategory.objects.all()
    # 计算出分类文章的数量，返回给前端。（这其中还可以添加筛选条件），注释部分是添加了筛选条件的，前端只需要读取num_articles，即可得出文章数量
    # category_list = Category.objects.filter(article__created_time_gt=(2015, 1, 1)).annotate(
    #     num_articles=Count('article')).filter(num_articles__gt=0)
    categories = ArticleCategory.objects.all().annotate(num_articles=Count('article')).all()

    context= {

        'categories':categories
    }

    return render(request,'cms/article_category.html',context=context)


# 添加文章分类
@require_POST
def add_acticle_category(request):
    # 单个字段不写表单,直接取值
    name = request.POST.get('name')
    # 验证表单是否存在
    exists = ArticleCategory.objects.filter(name=name).exists()
    if not exists:
        ArticleCategory.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message='该分类已经存在')



# 编辑文章分类
@require_POST
def edit_article_category(request):

    form = EditArticleCategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        name = form.cleaned_data.get('name')
        try:
            ArticleCategory.objects.filter(pk=pk).update(name=name)
            return restful.ok()
        except:
            return restful.params_error(message='该分类不存在')
    else:
        return restful.params_error(message=form.get_errors())


# 删除分类
@require_POST
def delete_article_category(request):
    pk = request.POST.get('pk')
    try:
        ArticleCategory.objects.filter(pk=pk).delete()
        return restful.ok()
    except:
        return restful.unauth(message='该分类不存在')


# 发布文章
class WriteArticle(View):
    # 处理get请求
    def get(self,request):
        categories = ArticleCategory.objects.all()
        context = {

            'categories': categories
        }
        return render(request,'cms/write_article.html',context=context)
    # 处理post请求
    def post(self,request):
        form = WriteArticleForm(request.POST)

        if form.is_valid():
            # 标题
            title = form.cleaned_data.get('title')
            # 描述信息
            desc = form.cleaned_data.get('desc')
            # 缩略图
            thumbnail = form.cleaned_data.get('thumbnail')
            # 主要内容
            content = form.cleaned_data.get('content')
            # 分类id
            category_id = form.cleaned_data.get('category')
            # 分类
            category = ArticleCategory.objects.get(pk=category_id)
            # 浏览数量
            look_quantity = form.cleaned_data.get('look_quantity')
            # 评论数量后期直接统计渲染到模板即可
            Article.objects.create(title=title,desc=desc,thumbnail=thumbnail,content=content,category=category,look_quantity=look_quantity,author=request.user)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())





#文章管理
class ArticleListView(View):

    def get(self,request):


        # 从前端获取相关参数
        page = int(request.GET.get('p', 1))
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        # request.GET.get(参数,默认值)
        # 这个默认值是只有这个参数没有传递的时候才会使用
        # 如果传递了，但是是一个空的字符串，那么也不会使用默认值
        category_id = int(request.GET.get('category',0) or 0)


        # 查询文章信息
        # 外键提前查询
        articles = Article.objects.select_related('category','author')


        # 如果可以获取到开始时间与结束时间,根据前端的时间参数进行查询,得到查询后的结果进行返回
        if start or end:
            if start:
                start_date = datetime.strptime(start,'%Y/%m/%d')
            else:
                start_date = datetime(year=2018,month=6,day=1)
            if end:
                end_date = datetime.strptime(end,'%Y/%m/%d')
            else:
                end_date = datetime.today()
            articles = articles.filter(pub_time__range=(make_aware(start_date),make_aware(end_date)))


        # 如果获取到title信息,根据查询到的title信息进行查询
        if title:
            articles = articles.filter(title__icontains=title)

        # 如果获取到分类信息,根据查询到的title信息进行查询
        if category_id:
            articles = articles.filter(category=category_id)

        # 传递可便利的对象,10表示每页显示的数量
        paginator = Paginator(articles,10)
        page_obj = paginator.page(page)

        context_data = self.get_pagination_data(paginator, page_obj)

        # 返回一些相关的参数,便于前端进行判断
        context = {
            'categories': ArticleCategory.objects.all(),
            'articles': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
            'start': start,
            'end': end,
            'title': title,
            'category_id': category_id,
            'url_query': '&'+parse.urlencode({
                'start': start or '',
                'end': end or '',
                'title': title or '',
                'category': category_id or ''
            })
        }
        context.update(context_data)
        return render(request,'cms/article_list.html',context=context)

    # 获取页数的相关信息
    def get_pagination_data(self, paginator, page_obj, around_count=2):

        # 当前页
        current_page = page_obj.number
        # 总页数
        num_pages = paginator.num_pages

        # 左边是否需要出现三个点
        left_has_more = False
        # 右边是否需要出现三个点
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        return {
            # left_pages：代表的是当前这页的左边的页的页码
            'left_pages': left_pages,
            # right_pages：代表的是当前这页的右边的页的页码
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }



# 编辑文章
class EditArticleView(View):
    def get(self,request):

        # 跟着文章id获取到所有文章字段信息
        article_id = request.GET.get('article_id')
        article = Article.objects.get(pk=article_id)
        context = {
            'article': article,
            'categories': ArticleCategory.objects.all()
        }
        return render(request,'cms/write_article.html',context=context)

    def post(self,request):
        form = EditArticleForm(request.POST)
        if form.is_valid():
            print("成功否?")
            # 标题
            title = form.cleaned_data.get('title')
            # 描述信息
            desc = form.cleaned_data.get('desc')
            # 缩略图
            thumbnail = form.cleaned_data.get('thumbnail')
            # 主要内容
            content = form.cleaned_data.get('content')
            # 分类id
            category_id = form.cleaned_data.get('category')
            pk = form.cleaned_data.get("pk")
            # 分类
            category = ArticleCategory.objects.get(pk=category_id)
            # 浏览数量
            look_quantity = form.cleaned_data.get('look_quantity')
            # 评论数量后期直接统计渲染到模板即可
            Article.objects.filter(pk=pk).update(title=title,desc=desc,thumbnail=thumbnail,look_quantity=look_quantity,content=content,category=category)
            print("成功否?")
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())





def delete_article(request):
    article_id = request.POST.get('article_id')
    Article.objects.filter(pk=article_id).delete()
    return restful.ok()



# 上传文件到服务器
@require_POST
def upload_file(request):
    # 获取文件
    file = request.FILES.get('file')
    # 获取文件名
    name = file.name
    # 保存到指定的文件夹，文件夹路径需要在settings中进行配置
    with open(os.path.join(settings.MEDIA_ROOT,name),'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    url = request.build_absolute_uri(settings.MEDIA_URL+name)
    # http://127.0.1:8000/media/abc.jpg
    return restful.result(data={'url':url})