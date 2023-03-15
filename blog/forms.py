from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from rest_framework import serializers


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image',
                  'gender',
                 'facebook',
                 'twitter',
                 'linkedin',
                 'website_link', 
                'about_you',
                ]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields =['category_name',
                'image',
                ] 

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields =['username',
                'first_name',
                'last_name',
                'email',
                ] 


class AdminRegister(UserCreationForm):
    class Meta:
        model = User
        fields =['username',
                'email',
                'is_superuser',
                ] 



class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
    	model = Comment
    	fields = ['body',]
        # image = serializers.FileField(use_url = True)

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username","first_name","last_name", "email","password1","password2")
        widgets={
        'last_name': forms.TextInput(attrs={'class': 'last_name'}),
        'password':  forms.PasswordInput(attrs={'class': 'password'}),
        
   		 }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =["category",
                    "title",
                    "image",
                    "text",]

class AdminPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =["category",
                    "title",
                    "image",
                    "text",
                    "publish",]


class Publish(forms.ModelForm):
    class Meta:
        model = Post
        fields =["publish",]


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'autofocus': 'on'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


    # def clean(self, *args, **kwargs):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')

    #     if username and password:
    #         user = authenticate(username=username, password=password)
    #         if not username:
    #             pass
    #         else: 
    #             raise forms.ValidationError('User Does Not Exist')
                
    #         if user.check_password(password):
    #             pass
    #         else:    
    #             raise forms.ValidationError('Incorrect Password')

    #         if user.is_active:
    #             pass
    #         else:
    #             raise forms.ValidationError('User account not acive')

    #     return super(LoginForm, self).clean(*args, **kwargs)