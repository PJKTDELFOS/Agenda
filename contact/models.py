from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

#id(primary key)
#first_name(string), last_name (string), phone (string)
#email(email), created_date (date), description (text)
#depois
#category (foreign key), show (boolean), owner(foreign key)
#picture (imagem)

class Contact(models.Model):#herdar de models
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    email=models.EmailField(max_length=254)
    created_date=models.DateTimeField(default=timezone.now)
    description=models.TextField(max_length=1800,blank=True)
    show=models.BooleanField(default=True)# bom para validação de cadastros
    picture=models.ImageField(blank=True,upload_to='pictures/%Y/%m/')


    def __str__(self):
        return f'{self.first_name} {self.last_name}'



