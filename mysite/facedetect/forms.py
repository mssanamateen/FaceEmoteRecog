from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class Register(UserCreationForm):
    email=forms.EmailField(required=True)
    # image=forms.ImageField(required=True)

    class Meta:
        model=User
        fields=("username","email","password1","password2")
    def save(self,commit=True):
        user=super(Register,self).save(commit=False)
        user.email=self.cleaned_data['email']
        # user.image=self.cleaned_data['image']
        if commit:
            user.save()
        return user

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
class SendQ(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


    