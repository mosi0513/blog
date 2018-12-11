from django import forms
from apps.forms import FormMixin




# 验证评论内容与文章id的表单
class PublicCommentForm(forms.Form,FormMixin):

    content = forms.CharField()
    article_id = forms.IntegerField()