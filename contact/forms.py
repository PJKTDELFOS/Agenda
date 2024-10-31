from django.core.exceptions import ValidationError
from . import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ContactForm(forms.ModelForm):
    #esse e o melhor forma do forms
    picture=forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept':'image/*'
            }
        )
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





























