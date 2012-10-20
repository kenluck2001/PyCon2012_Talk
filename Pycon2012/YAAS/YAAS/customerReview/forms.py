from django import forms
from YAAS.captcha.fields import CaptchaField

class ProductReviewForm(forms.Form):
    STATUS_CHOICES = (
		(1, 'Worst'),
		(2, 'Very bad'),
		(3, 'Fair'),
		(4, 'Good'),
		(5, 'Best'),
	)

    rating = forms.ChoiceField(label="Rating", choices=STATUS_CHOICES, widget=forms.RadioSelect)
    comment = forms.CharField(label="Comment", max_length=80, widget=forms.Textarea)
    captcha = CaptchaField()
