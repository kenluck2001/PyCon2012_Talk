from django import forms

class AdvertisementForm(forms.Form): 
	'''
		create advertisement
	'''
	name = forms.CharField(label="Name of Advert", max_length=30 )
	description = forms.CharField(label="Description", max_length=150, widget=forms.Textarea)
	image = forms.ImageField(label="Photo",required=False) 

	def clean_image(self):
		image = self.cleaned_data.get('image',False)
		if image:
			if image._size > 2.5*1024*1024:
				raise forms.ValidationError("Image file too large ( > 2.5mb )")
			return image
		else:
			raise forms.ValidationError("Couldn't read uploaded image")
