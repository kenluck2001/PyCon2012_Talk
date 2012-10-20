
from django import forms
from django.forms.widgets import PasswordInput
from YAAS.models import Bid, CustomUser
from YAAS import extra
from YAAS.captcha.fields import CaptchaField



class LoginForm(forms.Form):
	'''
		This is used to enable user login
	'''
	username = forms.CharField(label="Username", max_length=20)
	password = forms.RegexField(label="Password", regex=r'^(?=.*\W+).*$',widget=forms.PasswordInput, min_length=6)


	def __init__(self, request=None, *args, **kwargs):
		self.request = request
		super(LoginForm, self).__init__(*args, **kwargs)

	def clean(self):
		if self.request:
			if not self.request.session.test_cookie_worked():
				raise forms.ValidationError("Cookies must be enabled.")
		return self.cleaned_data


   
class RegistrationForm(forms.Form):
	'''
		This is used to register a new user who does not have an account.
	'''
	STATUS_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
	)
	user_name = forms.CharField(label="Username", max_length=20)
	pass_word = forms.RegexField(label="Password", regex=r'^(?=.*\W+).*$',widget=forms.PasswordInput, min_length=6,help_text='Password must be six characters long and contain at least one non-alphanumeric character.'
)
	retype_password = forms.RegexField(label="Password confirmation", regex=r'^(?=.*\W+).*$',widget=forms.PasswordInput, min_length=6, help_text='Password must be six characters long and contain at least one non-alphanumeric character.'
)
	email = forms.EmailField(label="Email", max_length="50")
	first_name = forms.CharField(label="First name", max_length=20)
	last_name = forms.CharField(label="Last name", max_length=20)
	phone_number = forms.CharField(label="Phone number", max_length=20)
	sex = forms.ChoiceField(label="Sex", choices=STATUS_CHOICES, widget=forms.RadioSelect)
	captcha = CaptchaField()

	def clean_pass_word(self):
		if self.data['pass_word'] != self.data['retype_password']:
			raise forms.ValidationError('Passwords do not match!')
		return self.data['pass_word']

	def isValidUsername(self):
		try:
			CustomUser.objects.get(username=self.data['user_name'])
			raise forms.ValidationError('The username is already taken. Please choose another')
		except:
			pass
		return

	def clean(self):
		self.clean_pass_word()
		self.isValidUsername()
		return self.cleaned_data 

class EditForm(forms.Form): 
	'''
		This is used to edit the form and this is used an interface.	
	'''
	STATUS_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
	)
	email = forms.EmailField(label="Email", max_length="50", required=False)
	first_name = forms.CharField(label="First name", max_length=20, required=False)
	last_name = forms.CharField(label="Last name", max_length=20, required=False)
	phone_number = forms.CharField(label="Phone number", max_length=20, required=False)
	sex = forms.ChoiceField(label="Sex", choices=STATUS_CHOICES, widget=forms.RadioSelect, required=False)
	captcha = CaptchaField()

class AuctionForm(forms.Form): 
    '''
		This is the form used to make an auction.
    '''
    name = forms.CharField(label="Auction name", max_length=30 )
    description = forms.CharField(label="Description", max_length=150, widget=forms.Textarea)
    minimum_price = forms.DecimalField(label="Minimum Price", max_digits=9, decimal_places=2)
    image = forms.ImageField(label="Photo") 
    captcha = CaptchaField()

    def clean_image(self):
        image = self.cleaned_data.get('image',False)
        if image:
            if image._size > 2.5*1024*1024:
                raise ValidationError("Image file too large ( > 2.5mb )")
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")

#Bid form not necessary
class BidForm(forms.Form):
	'''
		This is the form used to make a bid.
	'''
	amount = forms.DecimalField(max_digits=9, decimal_places=2)
	captcha = CaptchaField()

class PasswordForm(forms.Form):
	'''
		This is the form used to change password.
	'''
	old_password = forms.RegexField(label="Old Password", regex=r'^(?=.*\W+).*$',widget=forms.PasswordInput, min_length=6)

	new_password = forms.RegexField(label="New Password", regex=r'^(?=.*\W+).*$', widget=forms.PasswordInput, min_length=6)

	retype_newpassword = forms.RegexField(label="New Password Confirmation", regex=r'^(?=.*\W+).*$',widget=forms.PasswordInput, min_length=6)
	captcha = CaptchaField()

	def __init__(self, user=None, *args, **kwargs):
		self.user = user
		super(PasswordForm, self).__init__(*args, **kwargs)

	def clean_password(self):
		oldpass = self.cleaned_data['old_password']
		hashpw = extra.hashPassword(oldpass)
		valid = self.user.check_password(hashpw)
		if not valid:
			raise forms.ValidationError("Password Incorrect")


	def clean_pass_word(self):
		if self.data['new_password'] != self.data['retype_newpassword']:
			raise forms.ValidationError('Passwords do not match!')
		return self.data['new_password']

	def clean(self):
		self.clean_pass_word()
		return self.cleaned_data 
