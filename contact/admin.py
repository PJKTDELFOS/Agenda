from django.contrib import admin
from contact import models

# Register your models here.
@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display= ('id','first_name', 'last_name','phone',)
    ordering=('id',)
    search_fields=('id','description')
    
    

    

    

