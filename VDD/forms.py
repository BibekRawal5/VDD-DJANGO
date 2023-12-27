from django import forms

class ImageForm(forms.Form):
	img_field = forms.ImageField()
	
