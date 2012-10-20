from django import forms
from YAAS.captcha.fields import CaptchaField


class MessageForm(forms.Form):
	text = forms.CharField(label="Message",max_length=150 ,widget=forms.Textarea)
	captcha = CaptchaField()
  
