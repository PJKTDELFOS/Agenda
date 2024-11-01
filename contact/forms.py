from django.core.exceptions import ValidationError
from . import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation

class ContactForm(forms.ModelForm):
    #esse e o melhor forma do forms
    picture=forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept':'image/*'
            }
        ),required=False
    )
    first_name=forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'classe-a classe-b',
                'placeholder':'aqui veio do init'
            }

        ),
        # label='primeiro Nome'
        help_text='texto de ajuda para usuario'
    )

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    class Meta:
        model=models.Contact
        fields=(
            'first_name','last_name','phone',
            'email','description', 'category','picture'
                )
        widgets={
            'first_name':forms.PasswordInput()
        }
    def clean(self):
        cleaned_data=self.cleaned_data
        first_name=cleaned_data.get('first_name')
        last_name=cleaned_data.get('last_name')
        if first_name==last_name:
            self.add_error('first_name',
                ValidationError(
                    'primeiro nome e segundo iguais',
                    code='invalid'
                )
            )

        return super().clean()

    def clean_first_name(self):
        first_name=self.cleaned_data.get('first_name')
        if first_name =='ABC':
            self.add_error(
                'first_name',
                ValidationError(
                    'Mensagem erro 2', code='invalid'
                )
            )
        return first_name




class RegisterForm(UserCreationForm):
    first_name=forms.CharField(
        required=True,
        max_length=50,
        min_length=3,

    )
    email=forms.EmailField(
        required=True,
        max_length=150,
    )
    class Meta:
        model=User
        fields=(
            'first_name','last_name','email',
            'username','password1','password2',
        )
#logica para  localizar campos semelhantes
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error(
                    'email',ValidationError(
                        'ja existe esse email',
                                    code='invalid')
                )
        return email
class RegisterUpdateForm(forms.ModelForm):
    first_name=forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_lenght':'Por favor,add mais 2 letras'
        }
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
    )
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete":"new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False
    )
    password2 = forms.CharField(
        label='Password 2',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Use the same password as before',
        required=False
    )
    class Meta:
        model=User
        fields=(
            'first_name','last_name','email',
            'username',
        )
    def save(self,commit=True):
        cleaned_data=self.cleaned_data
        user=super().save(commit=False)
        password=cleaned_data.get('password1')

        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user



    def clean_email(self):
        email=self.cleaned_data.get('email')
        current_email=self.instance.email
        if current_email!= email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',ValidationError(
                        'ja existe esse email',
                                    code='invalid')
                )
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if  password1:
           try:
               password_validation.validate_password(password1)
           except ValidationError as errors:
               self.add_error('password1',
                              ValidationError(errors))

        return password1


    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1!=password2:
                self.add_error('password2',ValidationError('senha incorreta',
                                                           code='invalid'))

        return super().clean()
























