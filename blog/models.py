from django.db import models
from PIL import Image
# Create your models here.
import random
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from myblog.utils import unique_slug_generator
from ckeditor.fields import RichTextField

class Video(models.Model):
	video = models.FileField()
	title = models.CharField(max_length=3242)

	def videoURL(self):
		try:
			url = self.video.url
		except:
			url = ''
		return url
	
class Category(models.Model):
	category_name = models.CharField(max_length=93)
	image = models.ImageField()
	date  = models.DateTimeField(auto_now_add=True)
	approve = models.BooleanField(default=False)
	
	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url
	def __str__(self):
		return self.category_name
# choices = Category.objects.all().values_list('category_name', 'category_name')
# choice_list = []

# for item in choices:
# 	choice_list.append(item)
class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	date = models.DateTimeField(auto_now_add=True)
	image = models.ImageField()
	text = RichTextField()
	publish = models.BooleanField(default= False)
	slug = models.SlugField(max_length=2500, null=False, blank=True)
	likes = models.ManyToManyField(User, related_name='likes', blank=True)
	class Meta:
		db_table = "post"

	@property
	def num_likes(self):
		return self.likes.all().count()
	def __str__(self):
		return f'{self.title} || Post'
	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:	
			url = ''
		return url
	def save(self, *args, **kwargs):
		super(Post,self).save(*args, **kwargs)
		img = Image.open(self.image.path)
		if img.height < 1000 or img.width < 800:
			output_size = (1000, 800)
			img.thumbnail(output_size)
			img.save(self.image.path)
def slug_generator(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender= Post)

LIKE_CHOICES = [
	('Like', 'Like'),
	('Unlike', 'Unlike'),
]

class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=30)
	
	class Meta:
		db_table = "like"
	
	def __str__(self):
		return self.user.username
	
class Newsletter(models.Model):
	email = models.EmailField()

	def __str__(self):
		return self.email


class PostDetail(models.Model):
	post = models.OneToOneField(Post, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.post.title} || Post Details"




class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	gender = models.CharField(max_length=6, default = 'null', choices=(('Male', 'Male'), ('Female', 'Female')), blank=True)
	image = models.ImageField(default='avatar.png', max_length= 100)
	facebook = models.CharField(default='facebook', max_length= 100)
	twitter = models.CharField(default='twitter', max_length= 100)
	linkedin = models.CharField(default='linkedin', max_length= 100)
	website_link = models.URLField(default='https://www.abc.com')
	about_you = models.TextField()

	class Meta:
		db_table = "userprofile"

	def __str__(self):
		return f"{self.user.username} || Profile"
	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

	def save(self, *args, **kwargs):
		super(UserProfile,self).save(*args, **kwargs)
		img = Image.open(self.image.path)
		if img.height > 301 or img.width > 326:
			output_size = (301, 326)
			img.thumbnail(output_size)
			img.save(self.image.path)

class UserInfo(models.Model):
	username = models.CharField(max_length=40)
	password = models.CharField(max_length=40)
	agree = models.BooleanField(default=False)

	class Meta:
		db_table = "userinfo"

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	# reply = models.ForeignKey('self', null=True,on_delete=models.CASCADE)
	userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = "comment"
	def __str__(self):
		return f'{self.post.title} || Comment'


class Contact(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField(max_length=50)
	body = models.TextField()

	class Meta:
		db_table = "contact"