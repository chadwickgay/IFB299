class UserForm(forms, ModelForm):
	password = form.Charfied(widget = forms.PasswordInput)
	
class meta
	model = user
	fields = ['firstname','lastname','email','password','administrator']
	
