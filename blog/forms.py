from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from .models import Comment, BlogPost, Author, Category


class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'category', 'image']


class UpdateBlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'category', 'image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'body']

    def get_form_html(self):
        html = ''
        for field_name in self.Meta.fields:
            bound_field = self[field_name]
            html += f'<div class="form-group col-12">'
            if field_name == 'body':
                html += f'<label for="{field_name}">*Message</label>'
                html += f'<textarea name="{field_name}" id="{field_name}" rows="10" class="oleez-textarea" required></textarea>'
            else:
                html += f'{bound_field.as_widget(attrs={"class": "oleez-input"})}'
                html += f'<label for="{field_name}">{bound_field.label}</label>'
            html += '</div>'
        return mark_safe(html)


class SearchForm(forms.Form):
    query = forms.CharField(label="Search", max_length=100, required=False)
    author = forms.ModelChoiceField(label="Author", queryset=Author.objects.all(), required=False)
    category = forms.ModelChoiceField(label="Category", queryset=Category.objects.all(), required=False)


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User()
        fields = ["username", "password"]


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
