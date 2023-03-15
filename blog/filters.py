import django_filters
from .models import *
from django_filters import CharFilter
from django import forms

class PostFilter(django_filters.FilterSet):
	category = CharFilter(field_name='category', lookup_expr='icontains')
	title = CharFilter(field_name='title', lookup_expr='icontains')
	
	
	class Meta:
		model = Post
		fields = ['category', 'title']
		widget = {'category': forms.Textarea(attrs={'placeholders': 'Search here'}) }


class CategoryFilter(django_filters.FilterSet):
	category_name = CharFilter(field_name='category_name', lookup_expr='icontains')
	
	
	class Meta:
		model = Category
		fields = ['category_name']


class DetailsFilter(django_filters.FilterSet):
	class Meta:
		model = PostDetail
		fields = '__all__'
