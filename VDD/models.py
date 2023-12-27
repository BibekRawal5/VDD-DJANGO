from django.db import models
from django.utils.text import slugify 
import os
# Create your models here.
class ImageModel(models.Model):
	title=models.CharField(max_length=200)
	img=models.ImageField(upload_to="VDD/static/uploaded_images")
	
	def __str__(self):
		return self.title

	def filename(self):
		return os.path.basename(self.img.name)