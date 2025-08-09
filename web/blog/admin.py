from django.contrib import admin
from .models import Post
# ------ note -------------
# to use admin page, we need to create user in step called "Create Superuser"
# Superuser have all privileges (Add, Update, Delete)
# create superuser --> python manage.py createsuperuser 
# -------------------------
# Register your models here.
admin.site.register(Post) # register Model to show on admin page