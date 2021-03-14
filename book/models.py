from django.db import models
from django.conf import settings
from django.utils.text import slugify

# Create your models here.


class Book(models.Model):
	title = models.CharField(max_length=100, null=False, blank=False)
	author = models.CharField(max_length=100, null=False, blank=False)
	pdf = models.FileField(upload_to='books/pdfs', null=False, blank=False)
	date_uploaded = models.DateTimeField(auto_now_add=True, verbose_name = "date uploaded")
	uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
	# slug = models.SlugField(blank=True, unique=True)

	def __str__(self):
		return self.title
