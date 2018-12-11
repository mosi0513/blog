from django.db import models


# 分类模型
class ArticleCategory(models.Model):
    name = models.CharField(max_length=100)



# 文章模型
class Article(models.Model):
    # 标题
    title = models.CharField(max_length=200)
    # 描述信息
    desc = models.CharField(max_length=200)
    # 缩略图
    thumbnail = models.URLField()
    # 文本编辑器里面的内荣
    content = models.TextField()
    # 发布事件
    pub_time = models.DateTimeField(auto_now_add=True)
    # 分类 ,ForeignKey是一对多的关系
    category = models.ForeignKey('ArticleCategory',on_delete=models.SET_NULL,null=True)
    # 作者
    author = models.ForeignKey('mosiauth.User',on_delete=models.SET_NULL,null=True)
    # 观看数量
    look_quantity = models.CharField(max_length=100)
    # 评论数量
    comment = models.CharField(max_length=100)

    class Meta:
        # 时间排序
        ordering = ['-pub_time']



# 评论模型
class Comment(models.Model):
    # 用户名
    # CASCADE级联删除。当删除'一'时，‘多’会被删除。
    # 用户被删除掉了，那么这个评论也就会被删除
    author = models.ForeignKey("mosiauth.User", on_delete=models.CASCADE)
    # 评论的内容
    content = models.TextField()
    # 评论时间
    pub_time = models.DateTimeField(auto_now_add=True)
    # 文章 (哪一篇文章), 使用级联删除，新闻被删除，评论也会被删除
    article = models.ForeignKey('Article',on_delete=models.CASCADE,related_name='comments')

    class Meta:
        ordering = ['-pub_time']
