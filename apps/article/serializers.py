
# 导入序列化模块
from rest_framework import serializers
# 导入模型
from .models import Article,ArticleCategory,Comment

from apps.mosiauth.serializers import UserSerializers



# 文章分类的序列化
class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ('id','name')



# 创建一个文章类的序列化
class ArticleSerializer(serializers.ModelSerializer):
    # category 和author  由于建模型的时候是以外键的形式，所以要单独序列化
    category = ArticleCategorySerializer()
    author = UserSerializers()
    class Meta:
        model = Article
        fields = ('id','title','desc','thumbnail','pub_time','category','author','look_quantity')


class CommentSerizlizer(serializers.ModelSerializer):
    author = UserSerializers()
    class Meta:
        model = Comment
        fields = ('id','content','author','pub_time')
