from django import forms
from apps.forms import FormMixin
from apps.article.models import Article



# 编辑分类的表单
class EditArticleCategoryForm(forms.Form,FormMixin):
    pk = forms.IntegerField(error_messages={'required':'必须传入分类id'})
    name = forms.CharField(max_length=100)


# 发布文章的表单
class WriteArticleForm(forms.ModelForm,FormMixin):
    # 使用model.form来验证表单

    # 表单
    category = forms.IntegerField()
    class Meta:
        # 验证表单来自Article模型
        model = Article
        # 排除字段
        exclude = ['category','author','pub_time','comment']


# 编辑文章的表单
class EditArticleForm(forms.ModelForm,FormMixin):
    category = forms.IntegerField(error_messages={'required':'必须传入分类id'})
    pk = forms.IntegerField(error_messages={'required':'必须传入pk'})
    class Meta:
        model = Article
        exclude = ['category','author','pub_time','comment']
