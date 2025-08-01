from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.models import User,Group,Permission
from django import forms
import re

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username','password1', 'password2']:
            self.fields[fieldname].help_text = None
             

class CustomRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User

        fields = ['username', 'first_name', 'last_name', 'password1', 'confirm_password', 'email'] 

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errors = []

        if len(password1) < 8:
            errors.append('password must be at least 8 charecters long')
        
        if not re.search(r'[a-zA-Z0-9!@#$%^&*]', password1):
            errors.append('Password must include at least one special character.')
                
        if errors:
            raise forms.ValidationError(errors)

        return password1
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('confirm_password')

        if password1 != confirm_password:
            raise forms.ValidationError("password didn't match")
        return cleaned_data
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('this email is already existing')
        
        return email


class AssignedRoleForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label= 'Select a Role'
    )

    #ki j kori


class CreateGroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget= forms.CheckboxSelectMultiple,
        required=False,
        label='assign Permission'
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']



class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','first_name','last_name']

    bio = forms.CharField(required=False, widget=forms.Textarea)
    profile_picture = forms.ImageField(required=False)
    phone_number = forms.CharField(required=False,widget=forms.TextInput)

    def __init__(self,*args,**kwargs):
        self.userprofile = kwargs.pop('userprofile', None)
        super().__init__(*args,**kwargs)
        print( 'fomrs',self.userprofile)

        if self.userprofile:
            self.fields['bio'].initial = self.userprofile.bio
            self.fields['profile_picture'].initial = self.userprofile.profile_picture
            self.fields['phone_number'].initial = self.userprofile.phone_number

    def save(self,commit=True):
        user = super().save(commit=False)

        if self.userprofile:
            self.userprofile.bio = self.cleaned_data.get('bio')
            self.userprofile.profile_picture = self.cleaned_data.get('profile_picture')
            self.userprofile.phone_number = self.cleaned_data.get('phone_number')

            if commit:
                self.userprofile.save()
        if commit:
            user.save()
        
        return user
    


class CustomPasswordChangeForm(PasswordChangeForm):
    pass